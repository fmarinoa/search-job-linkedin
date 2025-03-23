from selenium.common import NoSuchElementException

from app.actions.BaseAction import wait_until_element_clickable
from app.utils.Constants import Constants


class SearchJob:
    def __init__(self, driver):
        self.driver = driver

    def scrape_jobs(self, job_description):
        print("Buscando trabajo para: " + job_description)

        wait_until_element_clickable(self.driver, Constants.TIME_OUT, "css selector", "#global-nav-typeahead input")

        job_description = job_description.replace(" ", "%20")

        self.driver.get(
            f"https://www.linkedin.com/jobs/search/?currentJobId=4189840029&f_TPR=r604800&keywords={job_description}&origin=JOB_SEARCH_PAGE_JOB_FILTER&spellCorrectionEnabled=true")

        xpath_base = "//*[@id='main']/*/*/*[1]/*[2]/ul/li"

        container = self.driver.find_element(by="xpath", value="//*[@id='main']/div/div[2]/div[1]/div")
        results = self.driver.find_elements(by="xpath", value=xpath_base)

        job_data = []
        for i in range(1, len(results) + 1):
            self.driver.implicitly_wait(2)
            if i == 1:
                self.driver.execute_script("arguments[0].scrollTop = 0", container)

            xpath_item = f"({xpath_base})[{i}]/*/*/*[1]/*[1]/*[2]/*"

            try:
                title_job = self.driver.find_element(by="xpath", value=xpath_item + "/a/span/strong").text
            except NoSuchElementException:
                self.driver.execute_script("arguments[0].scrollTop += 800", container)
                title_job = self.driver.find_element(by="xpath", value=xpath_item + "/a/span/strong").text

            link_job = self.driver.find_element(by="xpath", value=xpath_item + "/a").get_attribute("href")
            employer = self.driver.find_element(by="xpath", value=xpath_item + "[2]/span").text
            location = self.driver.find_element(by="xpath", value=xpath_item + "[3]/ul/li/span").text
            print(f"Index: {i}, Title: {title_job}, Employer: {employer}, Location: {location}, Link: {link_job}")
            job_data.append([i, title_job, employer, location, link_job])

        return job_data
