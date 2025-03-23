import os
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

project_path = Path().absolute()
today = datetime.now().strftime("%Y%m%d")

folder_path = str(project_path) + "/results/" + str(today)
timestamp = datetime.now().strftime("%H%M%S")


def capture_screenshot(driver, filename="screenshot"):
    """Captura una imagen del navegador y la guarda en la ruta matriz del proyecto."""

    # Crear nombre de archivo con timestamp para evitar sobrescribir
    file_path = os.path.join(f"{folder_path}/{filename}_{timestamp}.png")

    # Capturar y guardar la imagen
    driver.save_screenshot(file_path)
    print(f"📸 Captura guardada en: {file_path}")

    return file_path  # Retorna la ruta del archivo por si se necesita


def create_folder():
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Carpeta '{folder_path}' creada.")
    else:
        print(f"📁 La carpeta '{folder_path}' ya existe.")


def append_results_excel(results) -> None:
    # Crear un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.append(["Index", "Title Job", "Employer", "Location", "Link Job"])  # Encabezados

    for row in results:
        ws.append(row)

    # Guardar el archivo
    folder_to_save = f"{folder_path}/results_{timestamp}.xlsx"
    wb.save(folder_to_save)
    print(f"Archivo Excel guardado: {folder_to_save}")
