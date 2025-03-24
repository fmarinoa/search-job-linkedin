from pathlib import Path

import requests

from app.utils.logger_config import get_logger

logger = get_logger(__name__)

project_path = Path().absolute()
results_path = str(project_path) + "/results/"
html_path = f"{results_path}email_body.html"

url = "https://raw.githubusercontent.com/fmarinoa/search-job-linkedin/main/results/offers.json"

response = requests.get(url)
offers = response.json()

html_content = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; }
            .offer { margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
            .title { font-size: 18px; font-weight: bold; color: #333; }
            .company { color: #0073b1; }
            .link { text-decoration: none; color: #0073b1; }
        </style>
    </head>
    <body>
        <h2>Últimas Ofertas de Trabajo</h2>
        <p>Datos extraídos de https://github.com/fmarinoa/search-job-linkedin/tree/main/results</p>
    """

for offer in offers:
    html_content += f"""
        <div class="offer">
            <p class="title">{offer['Title job']}</p>
            <p><a class="link" href="{offer['Link profile employer']}">{offer['Employer']}</a></p>"""

    html_content += f"""<p><a class="link" href="{offer['Profile recruiter']}">{offer['Recruiter']}</a></p>""" if \
        offer['Recruiter'] else ""

    html_content += f"""
            <p>📍 {offer['Location']} | ⏳ {offer['How long ago']}</p>
            <p>{offer['Description offer'][:300]}...</p>
            <p><a class="link" href="{offer['Link offer']}">Ver oferta completa</a></p>
        </div>
        """

html_content += "</body></html>"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

logger.info(f"✅ html guardado en {html_path}'.")
