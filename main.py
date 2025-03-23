import os

from dotenv import load_dotenv

from app.utils.SearchJob import scrape_jobs
from app.utils.Util import create_folder, append_results_csv, append_results_json

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    load_dotenv()
    create_folder()

    results = scrape_jobs(
        os.getenv('JOB_DESCRIPTION', 'QA AUTOMATION'),
        os.getenv('LOCATION', 'LIMA PERÚ')
    )

    if results is None:
        raise ModuleNotFoundError("❌ Results es vació")

    append_results_csv(results)
    append_results_json(results)
