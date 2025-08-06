from pathlib import Path
from datetime import datetime
import pandas as pd

from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

logger = get_logger(__name__)

def get_day_folder_path() -> Path:
    """Devuelve la ruta results/año/mes/día y crea la carpeta si no existe."""
    now = datetime.now()
    day_path = Path(RESULTS_PATH) / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    day_path.mkdir(parents=True, exist_ok=True)
    return day_path

def save_results_csv(results: list[list], folder_path: Path) -> None:
    if not results or not isinstance(results, list) or not all(isinstance(row, list) for row in results):
        logger.error("❌ Los resultados no tienen el formato esperado: lista de listas.")
        return

    timestamp = datetime.now().strftime("%H%M%S")
    csv_path = folder_path / f"offers_{timestamp}.csv"

    headers, *data = results
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    logger.info(f"✅ CSV guardado en {csv_path}")

def append_results_csv(results: list[list]) -> None:
    """Guarda los resultados en la estructura results/año/mes/día/."""
    folder_path = get_day_folder_path()
    save_results_csv(results, folder_path)
