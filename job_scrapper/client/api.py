import json
import requests
from pathlib import Path
from typing import List, Dict

from job_scrapper.utils.config import load_config
from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

logger = get_logger(__name__)
config = load_config()

BASE_URL = config["api"]["endpoint"]
JSON_FILE = "offers.json"


def load_json(filepath: Path) -> List[Dict]:
    if not filepath.exists():
        logger.error(f"❌ Archivo no encontrado: {filepath}")
        return []

    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"❌ Error al decodificar JSON: {e}")
        return []


def send_offer(offer: Dict) -> None:
    try:
        response = requests.post(f"{BASE_URL}/job-offers/save", json=offer, timeout=60)
        if response.status_code == 201:
            logger.info(f"✅ Oferta cargada: {offer.get('titleJob', '[Sin título]')}")
        else:
            logger.warning(
                f"⚠️ Error {response.status_code} al cargar oferta '{offer.get('titleJob', '[Sin título]')}': {response.text}"
            )
    except requests.RequestException as e:
        logger.error(f"❌ Falló la solicitud para oferta '{offer.get('titleJob', '[Sin título]')}': {e}")


def send_offers_to_endpoint() -> None:
    json_path = Path(RESULTS_PATH) / JSON_FILE
    offers = load_json(json_path)

    if not offers:
        logger.warning("⚠️ No hay ofertas para procesar.")
        return

    logger.info(f"📦 Procesando {len(offers)} ofertas...")

    for offer in offers:
        send_offer(offer)
