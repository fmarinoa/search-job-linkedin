import json
import html
from pathlib import Path
from textwrap import dedent

from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

logger = get_logger(__name__)

HTML_PATH = Path(RESULTS_PATH) / "email_body.html"
JSON_PATH = Path(RESULTS_PATH) / "offers.json"

def generate_html():
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        offers = json.load(file)

    html_content = dedent("""\
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; }
                .offer { margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
                .title { font-size: 18px; font-weight: bold; color: #333; }
                .company, .link { color: #0073b1; text-decoration: none; }
            </style>
        </head>
        <body>
            <h2>Últimas Ofertas de Trabajo</h2>
            <p>Datos extraídos de 
            <a href="https://github.com/fmarinoa/search-job-linkedin/tree/main/results">
                GitHub Results
            </a></p>
    """)

    for offer in offers:
        title = html.escape(offer["titleJob"])
        employer = html.escape(offer["employer"])
        location = html.escape(offer["location"])
        time = html.escape(offer["howLongAgo"])
        description = html.escape(offer["descriptionOffer"][:300]) + "..."

        html_content += dedent(f"""\
            <div class="offer">
                <p class="title">{title}</p>
                <p><a class="link" href="{offer['linkProfileEmployer']}">{employer}</a></p>
        """)

        if offer.get("recruiter") and offer.get("profileRecruiter"):
            recruiter = html.escape(offer["recruiter"])
            html_content += f'<p><a class="link" href="{offer["profileRecruiter"]}">{recruiter}</a></p>'

        html_content += dedent(f"""\
                <p>📍 {location} | ⏳ {time}</p>
                <p>{description}</p>
                <p><a class="link" href="{offer['linkOffer']}">Ver oferta completa</a></p>
            </div>
        """)

    html_content += "</body></html>"

    HTML_PATH.write_text(html_content, encoding="utf-8")
    logger.info(f"✅ HTML generado en: {HTML_PATH}")
