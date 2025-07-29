import requests
import json
import re
import os
from app.utils.logger_config import get_logger

logger = get_logger(__name__)
BASE_URL = "https://job-offers-api-ujjz.onrender.com"
RESULTS_PATH = "./results"
JSON_FILE = "offers.json"

def to_camel_case(s: str) -> str:
    s = s.strip().lower()
    parts = re.split(r'[\s_]+', s)
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def load_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return []

def send_offer(offer: dict) -> None:
    camel_case_offer = {to_camel_case(k): v for k, v in offer.items()}
    try:
        response = requests.post(f"{BASE_URL}/job-offers/save", json=camel_case_offer, timeout=10)
        if response.status_code == 201:
            logger.info(f"✅ Offer loaded: {offer.get('Title job', 'Unknown')}")
        else:
            logger.warning(f"⚠️ Failed to load offer ({response.status_code}): {offer.get('Title job', 'Unknown')} - {response.text}")
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")

def main():
    json_path = os.path.join(RESULTS_PATH, JSON_FILE)
    offers = load_json(json_path)
    if not offers:
        logger.warning("No offers to process.")
        return

    logger.info(f"Processing {len(offers)} offers...")
    for offer in offers:
        send_offer(offer)

if __name__ == "__main__":
    main()