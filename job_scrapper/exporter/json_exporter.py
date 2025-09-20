import re
import pandas as pd
import json
from pathlib import Path

from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

logger = get_logger(__name__)

def to_camel_case(s: str) -> str:
    s = s.strip().lower()
    parts = re.split(r'[\s_]+', s)
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def append_results_json(results: list[list]) -> None:
    if not results or not isinstance(results, list) or not all(isinstance(r, list) for r in results):
        logger.error("❌ Formato inválido: se esperaba una lista de listas.")
        return

    json_path = Path(RESULTS_PATH) / "offers.json"

    headers = results[0]
    data = results[1:]
    camel_case_headers = {col: to_camel_case(col) for col in headers}

    df = pd.DataFrame(data, columns=headers)
    df.rename(columns=camel_case_headers, inplace=True)

    # Convertir a diccionarios para evitar doble serialización JSON
    records = df.to_dict(orient="records")
    
    # Serializar con separadores personalizados para evitar escape de barras
    json_data = json.dumps(records, indent=4, ensure_ascii=False, separators=(',', ': '))

    json_path.write_text(json_data, encoding="utf-8")

    logger.info(f"✅ JSON guardado en {json_path}")
