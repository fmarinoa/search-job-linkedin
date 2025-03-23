import os


class Login:
    def __init__(self, driver):
        self.driver = driver

    def login_submit(self):
        self.driver.find_element(by="id", value="username").send_keys(os.getenv('MAIL'))
        self.driver.find_element(by="id", value="password").send_keys(os.getenv('PASS'))

        if self.driver.find_element(by="id", value="rememberMeOptIn-checkbox").is_enabled():
            self.driver.find_element(by="xpath", value="//*[@id='rememberMeOptIn-checkbox']/../label").click()

        self.driver.find_element(by="xpath", value="//*[@id='organic-div']/form/div[4]/button").click()
