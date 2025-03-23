from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def wait_until_element_clickable(driver: WebDriver, time_out: int, by: str, value: str) -> WebElement:
    return WebDriverWait(driver, time_out).until(EC.element_to_be_clickable((by, value)))


def wait_until_element_element_located(driver: WebDriver, time_out: int, by: str, value: str) -> WebElement:
    return WebDriverWait(driver, time_out).until(EC.visibility_of_element_located((by, value)))
