import os
import json
import requests
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
from job_scrapper.utils.constants import RESULTS_PATH
from job_scrapper.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

FILTER_JSON_PATH = Path(RESULTS_PATH) / "filtered_offers.json"

def notify_whatsapp() -> None:
    """
    Lee las ofertas filtradas y las envía por WhatsApp usando la API de CallMeBot.
    """
    phone = os.getenv("WHATSAPP_PHONE")
    apikey = os.getenv("WHATSAPP_APIKEY")

    if not phone or not apikey:
        logger.info("ℹ️ WHATSAPP_PHONE o WHATSAPP_APIKEY no configurados. Omitiendo notificación por WhatsApp.")
        return

    if not FILTER_JSON_PATH.exists():
        logger.warning(f"⚠️ No se encontró el archivo de ofertas filtradas en: {FILTER_JSON_PATH}")
        return

    try:
        with open(FILTER_JSON_PATH, "r", encoding="utf-8") as f:
            offers = json.load(f)
    except Exception as e:
        logger.error(f"❌ Error al decodificar {FILTER_JSON_PATH}: {e}")
        return

    if not offers:
        logger.info("ℹ️ No hay ofertas de trabajo filtradas para notificar hoy.")
        return

    total = len(offers)
    max_display = 5
    
    # Formatear el mensaje
    message = "🤖 *Nuevas Ofertas de Trabajo Filtradas* 🤖\n\n"
    message += f"Hemos seleccionado *{total}* ofertas compatibles con tu perfil:\n\n"

    for idx, offer in enumerate(offers[:max_display], start=1):
        title = offer.get("title", "Sin título")
        employer = offer.get("employer", "Sin empresa")
        link = offer.get("linkOffer", "")
        reason = offer.get("reason", "")
        
        # Recortar razón para no saturar la pantalla de WhatsApp
        if reason and len(reason) > 150:
            reason = reason[:147] + "..."
            
        message += f"*{idx}. {title}* en *{employer}*\n"
        if reason:
            message += f"💡 *Razón:* {reason}\n"
        if link:
            message += f"🔗 {link}\n"
        message += "\n"

    if total > max_display:
        remaining = total - max_display
        message += f"➕ *Y {remaining} ofertas más.* Consulta el correo o GitHub para verlas todas."

    # Codificar mensaje para la URL
    encoded_message = urllib.parse.quote_plus(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_message}&apikey={apikey}"

    logger.info(f"📤 Enviando notificación por WhatsApp a {phone}...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            logger.info("✅ Notificación de WhatsApp enviada con éxito.")
        else:
            logger.error(f"❌ Error al enviar WhatsApp: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logger.error(f"❌ Error de red al comunicarse con CallMeBot: {e}")
