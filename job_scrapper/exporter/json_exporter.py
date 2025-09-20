import re
import pandas as pd
import json
from pathlib import Path
from urllib.parse import urlparse

from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

logger = get_logger(__name__)

def to_camel_case(s: str) -> str:
    s = s.strip().lower()
    parts = re.split(r'[\s_]+', s)
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def linkedin_clean_url(url: str) -> str:
    parsed = urlparse(url)
    match = re.search(r'/jobs/view/(?:[^/]*-)?(\d+)', parsed.path)
    if not match:
        return url
    job_id = match.group(1)
    return f"https://www.linkedin.com/jobs/view/{job_id}"

def append_results_json(results: list[list]) -> None:
    if not results or not isinstance(results, list) or not all(isinstance(r, list) for r in results):
        logger.error("❌ Formato inválido: se esperaba una lista de listas.")
        return

    json_path = Path(RESULTS_PATH) / "offers.json"

    headers = results[0]
    data = results[1:]
    camel_case_headers = {col: to_camel_case(col) for col in headers}

    df = pd.DataFrame(data, columns=headers)

    # Limpieza de links en columnas específicas
    cols_to_clean = ["Link offer"]
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].apply(linkedin_clean_url)

    df.rename(columns=camel_case_headers, inplace=True)

    # Convertir a diccionarios para evitar doble serialización JSON
    records = df.to_dict(orient="records")

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False, separators=(',', ': '))

    logger.info(f"✅ JSON guardado en {json_path} con {len(records)} ofertas")
