import os
from datetime import datetime
from pathlib import Path
import pandas as pd

from app.utils.logger_config import get_logger

project_path = Path().absolute()
today = datetime.now().strftime("%Y%m%d")

results_path = str(project_path) + "/results/"
today_path = results_path + str(today)

logger = get_logger(__name__)


def create_folder() -> None:
    if not os.path.exists(today_path):
        os.makedirs(today_path)
        logger.info(f"📁 Carpeta '{today_path}' creada.")
    else:
        logger.info(f"📁 La carpeta '{today_path}' ya existe.")


def append_results_csv(results: []) -> None:
    timestamp = datetime.now().strftime("%H%M%S")
    csv_path = f"{today_path}/offers_{timestamp}.csv"

    # Extraer encabezados de la primera fila y asignarlos a cada elemento
    headers = results[0]  # Primera fila como nombres de columnas
    data = results[1:]  # Datos reales

    # Crear DataFrame con encabezados correctos
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(csv_path, index=False, index_label=False, encoding="utf-8")
    logger.info(f"✅ CSV guardado en {csv_path}'.")


def append_results_json(results: []) -> None:
    json_path = f"{results_path}offers.json"

    # Extraer los nombres de las columnas y los datos
    headers = results[0]  # Primera fila son los nombres de columnas
    data = results[1:]  # Resto son los datos

    # Convertir en DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Convertir DataFrame a JSON sin caracteres escapados
    json_data = df.to_json(orient="records", indent=4, force_ascii=False)
    json_data = json_data.replace(r"\/", "/")

    # Guardar en un archivo JSON
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_data)

    logger.info(f"✅ json guardado en {json_path}'.")
