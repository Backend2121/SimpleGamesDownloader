from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import os
import json

class browser():
    def __init__(self):
        # Load config.json file
        with open("config.json",) as f:
            self.data = json.load(f)["SGD"]
            f.close()
        self.options = Options()
        self.options.add_argument("user-agent=Generic")
        self.options.add_argument("disable-popup-blocking")
        if self.data["adBlock"] == 1 or self.data["adBlock"] == "True": self.options.add_extension(os.path.normpath(os.getcwd() + "/Modules/adblock.crx"))
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + "/chromedriver", chrome_options=self.options)

    def start(self, link):
        self.driver.get(link)
        try:
            submitButton = WebDriverWait(self.driver, 120*60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/section/div/div/div/div/form/button')))
        except AttributeError:
            print("Ad redirect, retrying!")
            self.start(link)
        except WebDriverException:
            return "closed"
        submitButton.click()
        # Bypass fake robot check by insta-killing javascript with 4 ESCAPE inputs
        for x in range(0, 4):
            self.driver.execute_script("window.stop();")

        # Wait for 3 seconds to end with while loop
        finalLink = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
        while "javascript" in finalLink:
            finalLink = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
        self.driver.close()
        return finalLink
