import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai

from job_scrapper.exporter.csv_exporter import get_day_folder_path
from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

HTML_PATH = Path(RESULTS_PATH) / "email_body.html"
JSON_PATH = Path(RESULTS_PATH) / "offers.json"
FILTER_JSON_PATH = Path(RESULTS_PATH) / "filtered_offers.json"

RAW_DIR = get_day_folder_path() / "raw"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY no encontrada en variables de entorno")

client = genai.Client(api_key=GEMINI_API_KEY)

MAX_ATTEMPTS = int(os.getenv("GEMINI_MAX_ATTEMPTS", "3"))
BACKOFF_SECONDS = float(os.getenv("GEMINI_BACKOFF_SECONDS", "1.0"))
BATCH_SIZE = int(os.getenv("GEMINI_BATCH_SIZE", "25"))
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")


class GeminiAnalyzer:
    def __init__(self, profile_path: str = "config/profile.json") -> None:
        self.profile_path = profile_path
        self.profile = self._load_profile()

    def _load_profile(self) -> Dict[str, Any]:
        with open(self.profile_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def filter_offers(self) -> List[Dict[str, Any]]:
        """
        Divide las offers en batches, llama a Gemini por batch y consolida resultados.
        Devuelve una lista de matches deduplicada y guarda ./data/matches.json.
        """
        offers = []

        # Cargar las ofertas desde el archivo JSON_PATH
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            offers = json.load(f)

        # split en batches
        batches = [offers[i: i + BATCH_SIZE] for i in range(0, len(offers), BATCH_SIZE)]
        all_matches: List[Dict[str, Any]] = []
        seen_ids = set()

        for batch_idx, batch in enumerate(batches, start=1):
            prompt = self._build_prompt(batch, batch_idx, len(batches))
            batch_matches = self._call_gemini_with_retries(prompt, batch_idx)

            # Si la llamada falló pero no lanzó excepción (retorna []), seguimos con siguientes batches
            if not batch_matches:
                logger.info(f"[WARN] Batch {batch_idx}/{len(batches)} devolvió 0 matches")
                continue

            # normalizar y deduplicar por 'id' (fallback a linkOffer)
            for m in batch_matches:
                key = m.get("id") or m.get("linkOffer") or None
                if not key:
                    # si no hay id, crear key sintética
                    key = json.dumps(m, sort_keys=True)
                if key in seen_ids:
                    continue
                seen_ids.add(key)
                all_matches.append(m)

        # guardar resultado consolidado
        self._save_filtered_offers(all_matches)

    def _build_prompt(self, offers: List[Dict[str, Any]], batch_idx: int, total_batches: int) -> str:
        """
        Construye prompt limitado a los campos esenciales.
        Incluye info del batch para debugging.
        """
        profile_str = json.dumps(self.profile, ensure_ascii=False)
        offers_preview = [
            {"_id": o.get("_id"),
             "titleJob": o.get("titleJob"),
             "employer": o.get("employer"),
             "location": o.get("location"),
             "descriptionOffer": (o.get("descriptionOffer") or "")[:400],
             "linkOffer": o.get("linkOffer")}
            for o in offers
        ]

        return (
            "Eres un asistente que filtra ofertas de trabajo según un perfil profesional. "
            "No considerar puestos de asistente o juniors"
            "Analizar cuáles son las empresas más importantes en la región y darles prioridad.\n\n"
            "Perfil:\n"
            f"{profile_str}\n\n"
            f"Batch {batch_idx}/{total_batches} - Ofertas (campos: _id, titleJob, employer, location, descriptionOffer, linkOffer):\n"
            f"{json.dumps(offers_preview, ensure_ascii=False)}\n\n"
            "Tarea: Devuelve SOLO un JSON cuya raíz sea una LISTA. Cada elemento debe tener exactamente los campos:\n"
            '- "id": usar el valor de "_id" de la oferta (si no existe, usar linkOffer),\n'
            '- "title": titleJob,\n'
            '- "employer": employer,\n'
            '- "linkOffer": linkOffer,\n'
            '- "reason": breve explicación (1-2 frases) de por qué la oferta encaja con el perfil.\n\n'
            "En reason indicar el rango salaria si está en la oferta."
            "La respuesta debe ser estrictamente JSON (sin explicaciones adicionales). Si no hay matches, devuelve [] (una lista vacía).\n"
        )

    def _call_gemini_with_retries(self, prompt: str, batch_idx: int) -> List[Dict[str, Any]]:
        """
        Realiza la llamada a Gemini con reintentos y guarda raw responses en caso de error.
        Devuelve lista de matches (o [] si no hay matches).
        """
        backoff = BACKOFF_SECONDS

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                text = self._extract_text_from_response(response)
                if not text:
                    raise RuntimeError("Gemini devolvió contenido vacío (texto)")
                cleaned = self._clean_response_text(text)
                parsed = json.loads(cleaned)
                if not isinstance(parsed, list):
                    raise ValueError("Gemini devolvió JSON pero la raíz no es una lista")
                return parsed
            except Exception as e:
                self._handle_gemini_error(e, prompt, batch_idx, attempt, locals().get("response"))
                if attempt < MAX_ATTEMPTS:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                logger.info(f"[FAIL] batch {batch_idx} failed after {MAX_ATTEMPTS} attempts. Skipping this batch.")
                return []
        return []

    @staticmethod
    def _handle_gemini_error(error: Exception, prompt: str, batch_idx: int, attempt: int, response: Any = None) -> None:
        """
        Maneja el guardado de errores y respuestas crudas de Gemini.
        """
        ts = int(time.time())
        raw_path = RAW_DIR / f"raw_batch{batch_idx}_attempt{attempt}_{ts}.json"
        payload = {"error": repr(error), "attempt": attempt}
        try:
            payload["prompt_preview"] = prompt[:2000]
            payload["response_str"] = str(response) if response is not None else None
        except Exception:
            pass
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        logger.info(f"[ERROR] batch {batch_idx} attempt {attempt} failed: {error}. raw saved to {raw_path}")

    @staticmethod
    def _extract_text_from_response(response: Any) -> Optional[str]:
        """
        Intenta extraer el texto concatenado de response.candidates[0].content.parts.
        Devuelve None si no es posible.
        """
        candidates = getattr(response, "candidates", None)
        if not candidates:
            return None
        candidate = candidates[0]
        content_obj = getattr(candidate, "content", None)
        if content_obj is None:
            return None
        parts = getattr(content_obj, "parts", None)
        if not parts:
            return None
        texts = []
        for part in parts:
            text = getattr(part, "text", None)
            if text:
                texts.append(text)
        if not texts:
            return None
        return "".join(texts)

    @staticmethod
    def _clean_response_text(text: str) -> str:
        """
        Elimina fences de Markdown y comillas triple, devuelve texto listo para json.loads.
        """
        s = text.strip()

        # quitar ```json ... ``` o ``` ... ```
        if s.startswith("```json"):
            s = s[len("```json"):].strip()
        if s.startswith("```"):
            s = s[3:].strip()
        if s.endswith("```"):
            s = s[:-3].strip()

        # quitar triple quotes si hay
        if (s.startswith('"""') and s.endswith('"""')) or (s.startswith("'''") and s.endswith("'''")):
            s = s[3:-3].strip()

        return s

    @staticmethod
    def _save_filtered_offers(filtered: List[Dict[str, Any]]) -> None:
        FILTER_JSON_PATH.parent.parent.mkdir(parents=True, exist_ok=True)

        with open(FILTER_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ JSON filtrado guardado en: {FILTER_JSON_PATH}")
