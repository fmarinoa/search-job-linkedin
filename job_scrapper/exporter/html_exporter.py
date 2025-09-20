import json
import html
from pathlib import Path
from typing import Dict, List
from textwrap import dedent

from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

logger = get_logger(__name__)

HTML_PATH = Path(RESULTS_PATH) / "email_body.html"
JSON_PATH = Path(RESULTS_PATH) / "filtered_offers.json"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .offer {{
            margin-bottom: 20px;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .title {{
            font-size: 20px;
            font-weight: bold;
            color: #0a66c2;
            margin-bottom: 10px;
        }}
        .company {{
            color: #666;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        .reason {{
            color: #333;
            background-color: #f0f7ff;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        .link {{
            color: #0073b1;
            text-decoration: none;
            display: inline-block;
            padding: 8px 16px;
            background-color: #f0f7ff;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        .link:hover {{
            background-color: #e1efff;
        }}
        .no-offers {{
            text-align: center;
            padding: 20px;
            color: #666;
        }}
        h2 {{
            color: #283e4a;
            text-align: center;
            margin-bottom: 30px;
        }}
    </style>
</head>
<body>
    <h2>Últimas Ofertas de Trabajo Filtradas</h2>
    {content}
</body>
</html>
"""

def _render_offer(offer: Dict[str, str]) -> str:
    """
    Renderiza una oferta individual en HTML.

    Args:
        offer: Diccionario con los datos de la oferta

    Returns:
        str: HTML formateado para la oferta
    """
    title = html.escape(offer.get("title", "Sin título"))
    employer = html.escape(offer.get("employer", "Sin empresa"))
    link_offer = html.escape(offer.get("linkOffer", "#"))
    reason = html.escape(offer.get("reason", ""))

    return dedent(f"""
        <div class="offer">
            <p class="title">{title}</p>
            <p class="company">{employer}</p>
            <p class="reason">{reason}</p>
            <p><a class="link" href="{link_offer}" target="_blank">Ver oferta completa</a></p>
        </div>
    """)

def generate_html() -> None:
    """
    Genera un archivo HTML con las ofertas de trabajo filtradas.
    Lee las ofertas desde un archivo JSON y las formatea en HTML.
    """
    try:
        # Cargar las ofertas desde el archivo JSON
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            offers = json.load(f)

        # Preparar el contenido
        if not isinstance(offers, list):
            offers = [offers] if offers else []

        content = "".join(_render_offer(offer) for offer in offers) if offers else \
                 '<div class="no-offers"><p>No se encontraron ofertas que coincidan con el perfil.</p></div>'

        # Generar HTML final
        html_content = HTML_TEMPLATE.format(content=content)

        # Guardar archivo
        HTML_PATH.write_text(html_content, encoding="utf-8")
        logger.info(f"✅ HTML generado exitosamente en: {HTML_PATH}")

    except FileNotFoundError:
        logger.error(f"No se encontró el archivo de ofertas en {JSON_PATH}")
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar el archivo JSON en {JSON_PATH}")
    except Exception as e:
        logger.error(f"Error inesperado al generar HTML: {str(e)}")
