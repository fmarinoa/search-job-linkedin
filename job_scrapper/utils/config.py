import yaml
from pathlib import Path
from job_scrapper.utils.constants import SETTINGS_YAML

def load_config() -> dict:
    with open(Path(SETTINGS_YAML), "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        print(config) 
        return config
