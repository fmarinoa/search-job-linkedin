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
        data.append(["Title job", "Employer", "Link profile employer", "Location", "How long ago", "Recruiter",
                     "Profile recruiter", "Description offer", "Link offer"])

        for i in range(1, len(results) + 1):
            xpath_item = f"({xpath_base})[{i}]/*"
            title_job = tree.xpath(xpath_item + "/div[2]/h3")[0].text.strip()
            employer = tree.xpath(xpath_item + "/div[2]/h4/a")[0].text.strip()
            profile_employer = tree.xpath(xpath_item + "/div[2]/h4/a/@href")[0]
            location = tree.xpath(xpath_item + "/div[2]/div/span")[0].text.strip().replace('"', '')
            how_long_ago = tree.xpath(xpath_item + "/div[2]/div/time")[0].text.strip()
            link_job = tree.xpath(xpath_item + "/a/@href")[0]
            description_offer = get_description_offer(link_job)
            data.append([title_job, employer, profile_employer, location, how_long_ago, description_offer[0],
                         description_offer[1], description_offer[2], link_job])
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado: {e}")
        return

    return data


def get_description_offer(link: str) -> [str]:
    """ Obtiene la información de una oferta de trabajo.

    Retorna una lista con:
    1. Nombre del reclutador (o vacío si no existe)
    2. Link del perfil del reclutador (o vacío si no existe)
    3. Descripción completa del trabajo (sin cortes)
    """
    try:
        tree = html.fromstring(requests.get(link).content)

        # XPath de los 3 datos a extraer
        xpath_recruiter_name = "//*[@id='main-content']/section[1]/div/div/section[1]/div/div[1]/div/a/span/text()"
        xpath_recruiter_link = "//*[@id='main-content']/section[1]/div/div/section[1]/div/div[1]/div/a/@href"
        xpath_job_description = "//*[@id='main-content']/section[1]/div/div/section[1]/div/div[last()]/section/div"

        # Extraer datos o devolver ""
        recruiter_name = tree.xpath(xpath_recruiter_name)
        recruiter_link = tree.xpath(xpath_recruiter_link)
        job_description_node = tree.xpath(xpath_job_description)

        # Obtener todo el contenido del nodo (incluyendo texto dentro de etiquetas <br>, <strong>, etc.)
        job_description = job_description_node[0].xpath("string(.)").strip().encode('latin1').decode('utf-8') if job_description_node else ""

        return [
            recruiter_name[0].strip() if recruiter_name else "",
            recruiter_link[0].strip() if recruiter_link else "",
            job_description
        ]
    except Exception as e:
        logger.error(f"Error al obtener información de la oferta: {e}")
        return ["", "", ""]  # Si hay error, devuelve 3 valores vacíos
