from app.actions.Login import Login
from app.actions.SearchJob import SearchJob
from app.utils.Constants import Constants
from app.utils.Util import capture_screenshot, create_folder
from webdriver_factory.BrowserFactory import BrowserFactory

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    create_folder()
    driver = BrowserFactory.get_browser("chrome")
    driver.implicitly_wait(Constants.TIME_OUT)
    driver.get(Constants.URL_BASE)

    try:
        Login(driver).login_submit()
        search_job = SearchJob(driver)
        search_job.get_info("QA AUTOMATION")
    except Exception as e:
        print("Error inesperado: " + str(e))
        capture_screenshot(driver)
    finally:
        driver.quit()
