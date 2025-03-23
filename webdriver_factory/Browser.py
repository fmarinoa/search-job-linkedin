from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

from app.utils.Constants import Constants

# Configuración base para cualquier navegador
options = [
    "--disable-extensions",
    "--disable-gpu",
    "--disable-background-networking",
    "--disable-sync",
    "--metrics-recording-only",
    "--disable-default-apps",
    "--disable-notifications",
    "--disable-popup-blocking",
    "--disable-translate",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-client-side-phishing-detection",
    "--no-sandbox",
    "--start-maximized",
    "--headless",
    "--disable-dev-shm-usage"
]


def get_base_options():
    return options


class Browser:
    """Clase base para navegadores"""
    driver = None

    def get_driver(self):
        return self.driver


class ChromeBrowser(Browser):
    """Clase para Chrome"""

    def __init__(self):
        chrome_options = ChromeOptions()

        # Agregar optimizaciones
        for opt in get_base_options():
            chrome_options.add_argument(opt)

        self.driver = webdriver.Chrome(options=chrome_options)


class MsEdgeBrowser(Browser):
    """Clase para Edge"""

    def __init__(self):
        edge_options = EdgeOptions()

        # Agregar optimizaciones
        for opt in get_base_options():
            edge_options.add_argument(opt)

        self.driver = webdriver.Edge(options=edge_options)
