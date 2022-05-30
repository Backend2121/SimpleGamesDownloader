# TO BE USED ONLY TO DOWNLOAD LEGALLY BOUGHT GAMES

import sys
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
        self.name = "WowRoms"
        self.logPath = ""
        self.platformsArray = ["MAME 0.139u1", "Nintendo Gameboy Color", "Playstation", "Acorn Archimedes", "Acorn Electron", "Acorn Atom", "Amiga", "Apple I", "Apple II", "Apple II GS", "Atari 2600", "Atari 5200", "Atari 7800", "Atari 800", "Atari Jaguar", "Atari Lynx", "Atari ST", "Acorn BBC Micro", "Capcom Play System 1", "Capcom Play System 2", "Capcom Play System 3", "Commodore 64", "DOS", "Nintendo Famicom Disk System", "Future Pinball", "Nintendo Gameboy", "Nintendo Gameboy Advance", "Nintendo 64", "PC Engine/TurboGrafx 16", "PC Engine CD/Turbo Duo/TurboGrafx CD", "Neo Geo Pocket", "Neo Geo Pocket Color", "Neo Geo", "Nintendo DS", "Nintendo Entertainment System", "Nintendo Virtual Boy", "Nokia N Gage", "Playstation 2", "Playstation Portable", "Sega 32x", "Sega Genesis/MegaDrive", "Sega Master System", "Sega SG1000", "Sharp X68000", "Super Nintendo", "Windows 3.x", "Bandai Wonderswan", "Bandai Wonderswan Color", "ZX Spectrum", "Sinclair ZX81", "MAME", "Sega Game Gear", "MAME 0.37b5", "AMSTRAD CPC"]
        with open("config.json",) as f:
            try:
                self.data = json.load(f)[self.name]
            except KeyError:
                # Create/Load default config
                self.data = {
                    'isEnabled': 1,
                    'platform': 0,
                    'timeout': 10
                }
            f.close()

        # Main widget used to display all of this inside a tab
        self.widget = QWidget()

        # Define main layout used to house all the sub-layouts with respective tickBoxes/TextBoxes etc.
        self.mainLayout = QVBoxLayout()

        # Define sub-layouts
        self.tickBoxes = QVBoxLayout()
        self.listBoxes = QVBoxLayout()
        self.timeoutLabelBox = QHBoxLayout()

        # TickBoxes
        self.enableThis = QCheckBox("Enable module")
        self.timeoutBox = QLineEdit("Timeout Threshold")
        self.timeoutLabel = QLabel("Timeout threshold")
        self.timeoutBox.setToolTip("DEFAULT: 10.\nIncrease or decrease this number to change the amount of time the module will wait for the website to respond.\nSometimes WOWRoms hangs when giving the last link, increasing this number might fix the problem if it doesn;t the program will return to the user the furthest link it has reached")

        # Listbox + items add
        self.platformsList = QComboBox()
        self.platformsList.addItems(self.platformsArray)

        # Self-apply config.json
        self.enableThis.setChecked(bool(self.data["isEnabled"]))
        self.platformsList.setCurrentIndex(self.data["platform"])
        self.timeoutBox.setText(str(self.data["timeout"]))

        # Add everything to respective layouts
        self.tickBoxes.addWidget(self.enableThis)
        self.timeoutLabelBox.addWidget(self.timeoutLabel)
        self.timeoutLabelBox.addWidget(self.timeoutBox)
        self.tickBoxes.addLayout(self.timeoutLabelBox)
        self.listBoxes.addWidget(self.platformsList)

        # Add all layouts to mainLayout
        self.mainLayout.addLayout(self.tickBoxes)
        self.mainLayout.addLayout(self.listBoxes)

        # Give layout to widget
        self.widget.setLayout(self.mainLayout)

        # Define listeners
        self.enableThis.stateChanged.connect(self.stateChange)
        self.timeoutBox.textChanged.connect(self.stateChange)
        self.platformsList.currentIndexChanged.connect(self.stateChange)

    def stateChange(self) -> None:
        """Register changes to data array"""
        if self.enableThis.isChecked(): self.data["isEnabled"] = 1
        else: self.data["isEnabled"] = 0
        self.data["platform"] = self.platformsList.currentIndex()

        try:
            self.data["timeout"] = int(self.timeoutBox.text())
        except Exception:
            self.data["timeout"] = 1
            self.timeoutBox.setText(str(1))

class module:
    def __init__(self) -> None:
        # Instance of above Settings class
        self.preferences = Settings()

        self.name = self.preferences.name
        self.options = Options()

        # Define logger and set the default config for it
        self.log = logging.getLogger("WOWRoms_Logger")
        logging.basicConfig(filename=self.preferences.logPath , filemode='a', format='%(levelname)s - %(name)s - "%(asctime)s": %(message)s', level="INFO")

        # Headless + silent selenium config
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--headless")
        self.options.add_argument('log-level=1')

        # Windows chromedriver assignment
        if sys.platform == "win32":
            self.browser = Chrome(chrome_options=self.options, executable_path=os.getcwd() + "/chromedriver.exe")
        # Linux chromedriver assignment
        else:
            self.browser = Chrome(chrome_options=self.options, executable_path=os.getcwd() + "/chromedriver")
        

        # Base link to website read from config.json
        # Reformat link
        tempLink = self.preferences.platformsArray[self.preferences.data["platform"]]
        tempLink = tempLink.replace(" ", '%2B')
        self.link = 'https://wowroms.com/en/roms/list/{0}?search='.format(tempLink)
        # Variable to store what to search
        self.toSearch = ''
        # Arrays of games's icons and relative sizes if cropping is needed
        self.gamesicons = []
        self.sizes = []

        # Connection timeout to avoid endless waitings
        self.timeout = int(self.preferences.data["timeout"])

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
        # NEVER CALLED
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
        self.browser.get(self.link + self.toSearch + '&sort=download')
        gridContainer = self.browser.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/div[5]/ul")
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

    def listIcons(self) -> "tuple[list, list]":
        """Called by iconGamesWorker.py
        
        Instantiated in SEARCH PHASE 3 of gui.py"""
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
        self.browser.get(link)
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/section/div[2]/div[2]/div[1]/div[2]/div/div[2]/a[1]")))
        except TimeoutException as e:
            print("ERROR: Connection timed out ", e)
            self.log.exception("CONNECTION_TIMEOUT_EXCEPTION after {0} seconds. Returning furthest link reached: {1}".format(self.timeout, link))
            return (["Direct Download"], [str(link)])
        downloadButton = self.browser.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/div[2]/div[1]/div[2]/div/div[2]/a[1]").get_attribute("href")
        # Return the direct download link also with "Direct Download" string
        return (["Direct Download"], [str(downloadButton)])
        
    def cleanLink(self, link: str) -> str:
        # If a proxy is needed then this function will obtain the clear-text link (Refer to documentation for clarifications)
        """Called by cleanLinkWorker.py
        
        Instantiated in LINK_FETCHING PHASE 1 of gui.py"""
        link = link.replace(" Direct Download", "")
        return link
