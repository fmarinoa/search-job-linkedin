import requests
from lxml import html

from app.utils.logger_config import get_logger

logger = get_logger(__name__)


def scrape_jobs(job_description: str, location: str) -> []:
    logger.info("Locación a buscar: " + location)
    logger.info("Buscando trabajo para: " + job_description)

    data = []

    try:
        job_description = job_description.replace(" ", "%20")
        location = location.replace(" ", "%20")

        url = f"https://www.linkedin.com/jobs/search?keywords={job_description}&location={location}&f_TPR=r604800"

        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            logger.warn(f"❌ Error {response.status_code}: No se pudo acceder a la página")
            return

        tree = html.fromstring(response.content)

        xpath_base = "//*[@id='main-content']/section[2]/ul/li"

        results = tree.xpath(xpath_base)  # Obtiene todos los div con esa clase
        data.append(["Title job", "Employer", "Link profile employer", "Location", "How long ago", "Link offer"])

        for i in range(1, len(results) + 1):
            xpath_item = f"({xpath_base})[{i}]/*"
            title_job = tree.xpath(xpath_item + "/div[2]/h3")[0].text.strip()
            employer = tree.xpath(xpath_item + "/div[2]/h4/a")[0].text.strip()
            profile_employer = tree.xpath(xpath_item + "/div[2]/h4/a/@href")[0]
            location = tree.xpath(xpath_item + "/div[2]/div/span")[0].text.strip().replace('"', '')
            how_long_ago = tree.xpath(xpath_item + "/div[2]/div/time")[0].text.strip()
            link_job = tree.xpath(xpath_item + "/a/@href")[0]
            # print(f"Title: {title_job}, Employer: {employer}, Profile employer: {profile_employer}, Location: {location}, Link: {link_job}, Published ago: {how_long_ago}")
            data.append([title_job, employer, profile_employer, location, how_long_ago, link_job])
    except Exception as e:
        return data.append(f"Ocurrió un erro inesperado: {e}")

    return data
