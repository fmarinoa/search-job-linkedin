from app.actions.BaseAction import wait_until_element_clickable, wait_until_element_element_located
from app.utils.Constants import Constants


class SearchJob:
    def __init__(self, driver):
        self.driver = driver

    def get_info(self, job_description):
        wait_until_element_clickable(self.driver, Constants.TIME_OUT, "css selector", "#global-nav-typeahead input")

        job_description = job_description.replace(" ", "%20")

        self.driver.get(
            f"https://www.linkedin.com/jobs/search/?currentJobId=4189840029&f_TPR=r604800&keywords={job_description}&origin=JOB_SEARCH_PAGE_JOB_FILTER&spellCorrectionEnabled=true")

        xpath_base = "//*[@id='main']/*/*/*[1]/*[2]/ul/li"

        wait_until_element_element_located(self.driver, Constants.TIME_OUT, "xpath", xpath_base)

        container = self.driver.find_element(by="xpath", value="//*[@id='main']/div/div[2]/div[1]/div")
        results = self.driver.find_elements(by="xpath", value=xpath_base)
        for i in range(1, len(results) + 1):
            if i % 3 == 0:
                self.driver.execute_script("arguments[0].scrollTop += 300", container)

            xpath_item = f"({xpath_base})[{i}]/*/*/*[1]/*[1]/*[2]/*"
            title_job = self.driver.find_element(by="xpath", value=xpath_item + "/a/span/strong").text
            link_job = self.driver.find_element(by="xpath", value=xpath_item + "/a").get_attribute("href")
            employer = self.driver.find_element(by="xpath", value=xpath_item + "[2]/span").text
            location = self.driver.find_element(by="xpath", value=xpath_item + "[3]/ul/li/span").text

            print("Index: " + i)
            print("Title job: " + title_job)
            print("Employer: " + employer)
            print("Location: " + location)
            print("Link job: " + link_job)
