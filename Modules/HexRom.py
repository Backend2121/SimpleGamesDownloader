# TO BE USED ONLY TO DOWNLOAD LEGALLY BOUGHT GAMES

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
import os
import json
import logging
from PIL import Image

class Settings:
    def __init__(self) -> None:
        self.name = "HexRom"
        self.logPath = ""
        with open("config.json",) as f:
            try:
                self.data = json.load(f)[self.name]
            except KeyError:
                # Load default config
                self.data = {
                    'isEnabled': 1
                }
            f.close()

        # Main widget used to display all of this inside a tab
        self.widget = QWidget()

        # Define main layout used to house all the sub-layouts with respective tickBoxes/TextBoxes etc.
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
        """Register changes to data array"""
        if self.enableThis.isChecked(): self.data["isEnabled"] = 1
        else: self.data["isEnabled"] = 0

class module:
    def __init__(self) -> None:
        # Instance of above Settings class
        self.preferences = Settings()

        self.name = self.preferences.name
        self.options = Options()
        
        # Define logger and set the default config for it
        self.log = logging.getLogger("HexRom_Logger")
        logging.basicConfig(filename=self.preferences.logPath , filemode='a', format='%(levelname)s - %(name)s - "%(asctime)s": %(message)s', level="INFO")

        # Headless + silent selenium config
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--headless")
        self.options.add_argument('log-level=1')

        # Linux chromedriver assignment
        #self.browser = Chrome(chrome_options=self.options, executable_path=os.getcwd() + "/chromedriver")
        # Windows chromedriver assignment
        self.browser = Chrome(chrome_options=self.options, executable_path=os.getcwd() + "/chromedriver.exe")

        # Base link to website
        self.link = 'https://hexrom.com/roms/nintendo-3ds/?title='
        # Variable to store what to search
        self.toSearch = ''
        # Arrays of games's icons and relative sizes if cropping is needed
        self.gamesicons = []
        self.sizes = []

        # Connection timeout to avoid endless waitings
        self.timeout = 10

        # Initialization complete
        self.log.info("INITIALIZED {0}".format(self.name))

    def searchGame(self, game: str) -> None:
        """Called by searchGamesWorker.py
        
        Instantiated in SEARCH PHASE 1 of gui.py"""
        # Use this function to reach the website through a proxy if needed or use it as a set method for self.toSearch
        # Gets executed too fast so time sleep is needed
        time.sleep(1)
        self.toSearch = game
        return

    def cropImage(self, image: str, size: "tuple[int, int]") -> None:
        """Selenium screenshots the screen at a default resolution of 800x600 if "--headless" is used

        Size is a tuple containing height and width of the image

        ((800 - width)/2, (600 - height)/2) = top-left corner of icon

        top-left + width & height = Icon

        Grabs the game icon, removes the black borders"""
        boxArt = ((800-size[1])/2,(600-size[0])/2, (800-size[1])/2 + size[1], (600-size[0])/2 + size[0])
        img = Image.open(image, mode="r")
        cropped = img.crop(boxArt)

        # Remove old image
        os.remove(image)

        try:
            # Save cropped image
            cropped.save(image)

        except SystemError as e:
            self.log.error("Error in cropping image: {0}".format(e))

    def listGames(self) -> "tuple[list, list]":
        """Called by listGamesWorker.py
        
        Instantiated in SEARCH PHASE 2 of gui.py

        Gets all games listed in the first page of results

        tuple[0] = Games's Titles

        tuple[1] = Games's Links
        """
        titlesLinks = [],[]
        self.browser.get(self.link + self.toSearch + '&genre=&region=')
        gridElement = self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div/div")
        for element in gridElement.find_elements_by_css_selector("div"):
            if element.get_attribute('title'):
                titlesLinks[0].append(element.get_attribute('title'))
                titlesLinks[1].append(element.get_attribute('href'))

        return titlesLinks

    def listIcons(self) -> "tuple[list, list]":
        """Called by iconGamesWorker.py
        
        Instantiated in SEARCH PHASE 3 of gui.py"""
        gridElement = self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div/div")
        for game in gridElement.find_elements_by_css_selector("div"):
            if game.get_attribute("class") == "thumbnail icon-post":
                img = game.find_element_by_css_selector("img")
                self.gamesicons.append(img.get_attribute('src'))
                self.sizes.append((int(img.get_attribute('naturalHeight')),int(img.get_attribute('naturalWidth'))))
        return (self.gamesicons, self.sizes)

    def download(self, link: str) -> None:
        # NEVER CALLED IN THIS EXAMPLE
        """Can be used to automatically download a game/rom if possible"""
        self.browser.get(link)
        WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div[2]/div/h1[2]/a")))
        # Need to find a way to ensure that the download is completed, then close the browser (unelegant solution: wait 10 seconds and hope the download is complete)
        time.sleep(10)
        self.browser.close()

    def listLinks(self, link: str) -> "tuple[list, list]":
        """Called by listLinksWorker.py
        
        Instantiated in SELECTION PHASE 1 of gui.py"""
        link = link + "download/"
        self.browser.get(link)
        self.titles = []
        self.downloadLinks = []
        
        table = self.browser.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/div/div[2]/div/table")
        for a in table.find_elements_by_css_selector("a"):
            self.titles.append(a.text)
            self.downloadLinks.append(a.get_attribute("href"))
        # Return the direct download link also with "Direct Download" string
        return (self.titles, self.downloadLinks)
        
    def cleanLink(self, link: str) -> str:
        # If a proxy is needed then this function will obtain the clear-text link (Refer to documentation for clarifications)
        """Called by cleanLinkWorker.py
        
        Instantiated in LINK_FETCHING PHASE 1 of gui.py"""
        for l in self.titles:
            if l in link:
                link = link.replace(l, "")
        return link
