from job_scrapper.client.api import send_offers_to_endpoint
from job_scrapper.exporter.csv_exporter import append_results_csv
from job_scrapper.exporter.html_exporter import generate_html
from job_scrapper.exporter.json_exporter import append_results_json
from job_scrapper.scrapper import scrape_jobs

def main():
    results = scrape_jobs()

    if results is None or not results or len(results) < 2:
        raise ValueError("❌ 'results' está vacío o no contiene datos suficientes.")

    append_results_csv(results)
    append_results_json(results)
    generate_html()
    send_offers_to_endpoint()


if __name__ == "__main__":
    main()
