import os

from dotenv import load_dotenv

from app.actions.Login import Login
from app.actions.SearchJob import SearchJob
from app.utils.Constants import Constants
from app.utils.Util import capture_screenshot, create_folder, append_results_excel
from webdriver_factory.BrowserFactory import BrowserFactory

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    load_dotenv()
    create_folder()
    browser = os.getenv('BROWSER', 'chrome')
    print("Ejecutando en: " + str(browser))
    driver = BrowserFactory.get_browser("chrome")
    driver.implicitly_wait(Constants.TIME_OUT)
    driver.get(Constants.URL_BASE)

    try:
        Login(driver).login_submit()
        search_job = SearchJob(driver)
        results = search_job.scrape_jobs(os.getenv('JOB_DESCRIPTION', 'QA AUTOMATION'))

        if results is None:
            raise FileNotFoundError("Results está vació")

        append_results_excel(results)
    except Exception as e:
        print("Error inesperado: " + str(e))
        capture_screenshot(driver)
    finally:
        driver.quit()
