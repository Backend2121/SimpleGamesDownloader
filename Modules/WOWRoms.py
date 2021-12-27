from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import json
import os
import logging

from PIL import Image

class Settings():
    """WOWRoms Settings"""
    def __init__(self) -> None:
        self.name = "WOWRoms"
        self.logPath = os.path.normpath(os.getcwd() + "//ReplaceWithTime.log")
        with open("config.json",) as f:
            try:
                self.data = json.load(f)[self.name]
            except KeyError:
                # Load default config
                self.data = {
                    'isEnabled': 1
                }
        
        # Main widget used to display all of this inside a tab
        self.widget = QWidget()

        # Define main layout used to house all the sub-layouts
        self.mainLayout = QVBoxLayout()

        # Define sub-layouts
        self.tickBoxes = QVBoxLayout()

        # TickBoxes
        self.enableThis = QCheckBox("Enable module")

        # Add everything to respective layouts
        self.tickBoxes.addWidget(self.enableThis)

        # Add all layouts to mainLayout
        self.mainLayout.addLayout(self.tickBoxes)

        # Give layout to widget
        self.widget.setLayout(self.mainLayout)

        # Define listeners
        self.enableThis.stateChanged.connect(self.stateChange)

        # Self-apply config.json
        self.enableThis.setChecked(bool(self.data["isEnabled"]))

    def stateChange(self) -> None:
        """Register changes to config.json"""
        if self.enableThis.isChecked(): self.data["isEnabled"] = 1
        else: self.data["isEnabled"] = 0

class module:
    def __init__(self) -> None:
        self.preferences = Settings()
        self.name = self.preferences.name
        self.options = Options()
        self.log = logging.getLogger("WOWRoms_Logger")
        
        logging.basicConfig(filename=self.preferences.logPath , filemode='a', format='%(levelname)s - %(name)s - "%(asctime)s": %(message)s', level="INFO")

        # Auto-Download settings
        #self.options.add_experimental_option("prefs", {
        #"download.default_directory": os.getcwd(),
        #"download.prompt_for_download": False,
        #"download.directory_upgrade": True,
        #"safebrowsing.enabled": True
        #})
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--headless")
        self.options.add_argument('log-level=1')

        #self.browser = Chrome(chrome_options=self.options, executable_path=os.getcwd() + "/chromedriver")
        self.browser = Chrome(chrome_options=self.options, executable_path=os.getcwd() + "/chromedriver.exe")
        self.link = 'https://wowroms.com/en/roms/list/Nintendo%2BGameboy%2BAdvance?search='
        self.toSearch = ''
        self.gamesicons = []
        self.sizes = []
        self.timeout = 10

        self.log.info("INITIALIZED {0}".format(self.name))

    def searchGame(self, game: str) -> None:
        # Gets executed too fast so time sleep is needed
        time.sleep(1)
        self.toSearch = game
        return

    def cropImage(self, image, size):
        # Selenium screenshots the screen at a default resolution of 800x600
        # Size is a tuple containing height and width
        # ((800 - width)/2, (600 - height)/2) = top-left corner of icon
        # top-left + width & height = Icon
        """Grabs the game icon, removes the black borders"""
        boxArt = ((800-size[1])/2,(600-size[0])/2, (800-size[1])/2 + size[1], (600-size[0])/2 + size[0])
        img = Image.open(image, mode="r")
        cropped = img.crop(boxArt)
        os.remove(image)
        try:
            cropped.save(image)
        except SystemError as e:
            print("Error: " + e)


    def listGames(self) -> tuple[list, list]:
        """Gets all games listed in the first page of results

        tuple[0] = Games's Titles

        tuple[1] = Games's Links
        """
        titlesLinks = [],[]
        self.log.info("Searching for {0} in {1}".format(self.toSearch, self.link + self.toSearch + '&sort=download'))
        self.browser.get(self.link + self.toSearch + '&sort=download')
        self.log.info("Website reached")
        gridContainer = self.browser.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/div[5]/ul")
        self.log.info("Element found")
        # Contains all information about a game: title, link and icon
        games = gridContainer.find_elements_by_tag_name("li")
        for x in games:
            # Get game's title
            if x.get_attribute("data-alpha") != None:
                titlesLinks[0].append(x.get_attribute("data-alpha"))

                # Find the first occurrence of the game's link
                for y in x.find_elements_by_tag_name("a"):
                    titlesLinks[1].append(y.get_attribute("href"))
                    break

                # Find the first occurrence of the game's icon
                for z in x.find_elements_by_tag_name("img"):
                    # This while loop "waits" for the images to have a size different from (0,0) (which means they have not loaded yet)
                    while z.get_attribute("naturalHeight") == "0":
                        continue
                    # Append games icons and icon sizes to each respective array
                    self.gamesicons.append(z.get_attribute("src"))
                    self.sizes.append((int(z.get_attribute("naturalHeight")),int(z.get_attribute("naturalWidth"))))
                    #print((int(z.get_attribute("naturalHeight")),int(z.get_attribute("naturalWidth"))))
                    break
        return titlesLinks

    def listIcons(self):
        return (self.gamesicons, self.sizes)

    def download(self, link):
        self.browser.get(link)
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div[2]/div/h1[2]/a")))
        # Need to find a way to ensure that the download is completed, then close the browser
        time.sleep(10)
        self.browser.close()
        # We need to wait 5 seconds to download the rom

    def listLinks(self, link):
        self.browser.get(link)
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div[2]/div[1]/div[2]/div/div[2]/a[1]")))
        except TimeoutException as e:
            print("ERROR: Connection timed out ", e)
            return (["CONNECTION_TIMEOUT_EXCEPTION"], "null")
        downloadButton = self.browser.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/div[2]/div[1]/div[2]/div/div[2]/a[1]").get_attribute("href")
        # Return the direct download link also with "Direct Download" string
        return (["Direct Download"], [str(downloadButton)])
        
    def cleanLink(self, link):
        link = link.replace(" Direct Download", "")
        return link