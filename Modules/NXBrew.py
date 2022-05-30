# TO BE USED ONLY TO DOWNLOAD LEGALLY BOUGHT GAMES

import os
import json
import time
from typing import Tuple
import logging

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Modules.Extras import manualCaptcha
from Modules.Workers.adBlockerDownloaderWorker import adBlockerDownloaderWorker

from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

from bs4 import BeautifulSoup

proxy = "https://hide.me/it/proxy"
# Chrome headless and silent options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('user-agent=Generic')

class Settings():
    """SGD Settings"""
    def __init__(self) -> None:
        self.name = "NXBrew"
        self.logPath = os.path.normpath(os.getcwd() + "//ReplaceWithTime.log")
        # Load config.json file
        with open("config.json",) as f:
            try:
                self.data = json.load(f)[self.name]
            except KeyError:
                # Load default config
                self.data = {
                    "isEnabled": 1,
                    "semiAutoMode": 0,
                    "adBlock": 0,
                    "useProxy": 1
                }
        # Widget
        self.widget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.topCenter = QVBoxLayout()
        self.tickBoxes = QGridLayout()
        self.buttonLayout = QVBoxLayout()

        # Build mainLayout
        self.mainLayout.addLayout(self.topCenter)
        self.mainLayout.addLayout(self.tickBoxes)
        self.mainLayout.addLayout(self.buttonLayout)

        # Set mainLayout
        self.widget.setLayout(self.mainLayout)

        # TickBoxes
        self.semiAuto = QCheckBox("Semi-auto mode")
        self.adBlocker = QCheckBox("AdBlocker")
        self.enableThis = QCheckBox("Enable module")
        self.useProxy = QCheckBox("Use Proxy")

        # Assign to layout
        self.tickBoxes.addWidget(self.enableThis, 0, 0)
        self.tickBoxes.addWidget(self.adBlocker, 1, 0)
        self.tickBoxes.addWidget(self.semiAuto, 2, 0)
        self.tickBoxes.addWidget(self.useProxy, 3, 0)

        # Self-apply config.json
        self.semiAuto.setChecked(bool(self.data["semiAutoMode"]))
        self.adBlocker.setChecked(bool(self.data["adBlock"]))
        self.enableThis.setChecked(bool(self.data["isEnabled"]))
        self.useProxy.setChecked(bool(self.data["useProxy"]))

        # Set tooltips 
        self.semiAuto.setToolTip("ON: The user will be asked to solve the Captcha, once solved the script will continue on it's own<br>OFF: The program will only reach the Captcha page, you will need to continue on your own")
        self.adBlocker.setToolTip("ON: Disables intrusive ads ONLY in Captcha page<br>OFF: Renders ALL the ads in the Captcha page<br>Personal Note: Leave this unchecked as ads supports the website's owner(s)")
        self.useProxy.setToolTip("ON: Use hide.me as proxy to access NXBrew.com in blocked regions<br>OFF: Bypass hide.me's proxy if you can access this website directly")

        # Define listeners
        self.semiAuto.stateChanged.connect(self.stateChange)
        self.adBlocker.stateChanged.connect(self.stateChange)
        self.enableThis.stateChanged.connect(self.stateChange)
        self.useProxy.stateChanged.connect(self.stateChange)

    def stateChange(self):
        if self.semiAuto.isChecked(): self.data["semiAutoMode"] = 1
        else: self.data["semiAutoMode"] = 0

        if self.enableThis.isChecked(): self.data["isEnabled"] = 1
        else: self.data["isEnabled"] = 0

        if self.useProxy.isChecked(): self.data["useProxy"] = 1
        else: self.data["useProxy"] = 0

        if self.adBlocker.isChecked():
            self.data["adBlock"] = 1
            if (os.path.isfile(os.path.normpath(os.getcwd() + "/Modules/adblock.crx"))):
                pass
            else:
                # Define message box + layout
                self.downloadAdBlockerMessage = QMessageBox()
                self.downloadAdBlockerMessageLayout = self.downloadAdBlockerMessage.layout()
                
                # Define messageBox default button
                self.closeButton = QPushButton(" Close")
                self.downloadAdBlockerMessage.addButton(self.closeButton, QMessageBox.YesRole)

                # Define and set ProgressBar
                self.pbar = QProgressBar()
                self.downloadAdBlockerMessageLayout.addWidget(self.pbar, 1, 0)

                # Set window stuff
                self.downloadAdBlockerMessage.setWindowTitle("Downloading...")
                self.adBlockLabel = QLabel("Getting the AdBlocker for you <3!")
                self.downloadAdBlockerMessageLayout.addWidget(self.adBlockLabel, 0, 0)
                # Load gui configs
                with open("config.json",) as f:
                    self.generalData = json.load(f)["General"]
                    f.close()   
                self.downloadAdBlockerMessage.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.generalData["theme"] + ".css"), "r").read())

                # Start adBlocker downloader worker
                self.adBlockerDownloader = adBlockerDownloaderWorker()
                self.adBlockerDownloader.start()
                self.adBlockerDownloader.updated.connect(self.closeDownloadingAdBlocker)
                self.closeButton.setEnabled(False)

                # Execute
                self.downloadAdBlockerMessage.exec_()
        else:
            self.data["adBlock"] = 0
        
    def closeDownloadingAdBlocker(self, value):
        self.pbar.setValue(value)
        if (value >= 99):
            self.closeButton.setEnabled(True)
            self.downloadAdBlockerMessage.close()

class module():
    """NXBrew main class"""
    def __init__(self) -> None:
        """Instantiate the Selenium browser, used throughout the entire process"""
        self.name = "NXBrew"
        self.preferences = Settings()
        self.log = logging.getLogger("NXBrew_Logger")
        logging.basicConfig(filename=self.preferences.logPath , filemode='a', format='%(levelname)s - %(name)s - "%(asctime)s": %(message)s', level="INFO")

        try:
            #self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
            self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.getcwd() + "/chromedriver")
        except:
            self.log.fatal("NO WEBDRIVER FOUND EXITING!")

        self.log.info("INITIALIZED {0}".format(self.name))

    def Proxy(self, URL: str, call: bool) -> None:
        """Navigate hide.me website"""
        # Tunnel with Proxy
        self.browser.get(proxy)
        inputBox = self.browser.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div[2]/div/form/fieldset/div[1]/input')
        self.browser.delete_all_cookies()
        
        inputBox.click()
        inputBox.clear()
        inputBox.send_keys(URL)
        # Disable url encryption
        settings = self.browser.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div[2]/div/form/fieldset/div[2]/div[2]/button')
        settings.click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div/div[2]/div/form/fieldset/div[2]/div[2]/div/ul/li[2]/label/input").click()
        try:
            inputBox.submit()
            # Redirected to NxBrew.com
            if call:
                return self.scrape(self.browser.page_source)
        except:
            self.log.warning("Weird long error, ignoring")
            if call:
                return self.scrape(self.browser.page_source)

    def cleanLink(self, userInput: str) -> str:
        """Final step: Unpoison download link"""
        print("User Input: " + userInput)
        # User error checking
        if "/go.php" not in userInput:
            start = userInput.find("http")
            if start == -1:
                return
            return userInput[start:]
        # Link skippin'
        if self.preferences.data["useProxy"] == 1:
            userInput = userInput[userInput.find("/go.php"):]
            self.browser.get("https://nl.hideproxy.me" + userInput)
            downloadLink = self.browser.find_element_by_xpath("/html/body/header/div/div/div/div[1]/a").get_attribute("href")
            self.browser.get(downloadLink)
            unpoisonedLink = self.browser.find_element_by_xpath('/html/body/div[1]/form/div/input').get_attribute("value")
        else:
            unpoisonedLink = userInput
        # Semi automatic mode check
        if self.preferences.data["semiAutoMode"] == 1:
            self.b = manualCaptcha.browser()
            self.log.info("Cleaned link: {0}".format(unpoisonedLink))
            return self.b.start(unpoisonedLink)
        else:
            self.log.info("Cleaned link: {0}".format(unpoisonedLink))
            return unpoisonedLink

    # REGION Pre Captcha
        self.browser.get(unpoisonedLink)
        
        # Bypass fake robot check by insta-killing javascript with 4 ESCAPE inputs
        for x in range(0, 4):
            self.browser.execute_script("window.stop();")

        # Wait for 3 seconds to end with while loop
        finalLink = self.browser.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
        while "javascript" in finalLink:
            finalLink = self.browser.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
        
        return finalLink# ENDREGION
    def scrape(self, htmlPage: str) -> Tuple[list, list]:
        """Find all link available for a certain title"""
        # Contains hrefs poisoned by hide.me
        self.downloadLinks = []
        self.downloadLabels = []
        self.result = [],[]
        # result[0] = Download name result[1] = Download name + link
        # Step by step garbage cleaning of html page with BS4
        soup = BeautifulSoup(htmlPage, 'html.parser')
        for bigDiv in soup.find_all("div", class_="wp-block-columns has-2-columns"):
            for div in bigDiv.find_all("div", class_="wp-block-column"):
                for p in div.find_all("p"):
                    # Get download name
                    try:
                        self.result[0].append(p.find("strong").get_text())
                        self.result[1].append("- ")
                    except:
                        pass
                    # Get download name + link
                    for a in p.find_all("a"):
                        self.result[0].append(a.get("href"))
                        self.result[1].append(a.get_text())
        self.log.info("RESULTS ARRAY: {0}".format(self.result[0]))
        return self.result

    def searchGame(self, toSearch: str) -> None:
        """First step: Reach nxbrew with proxy if useProxy is eneabled"""
        # Reset Chromedriver
        try:
            self.browser.close()
            #self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
            self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver", chrome_options=chrome_options)
        except:
            #self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
            self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver", chrome_options=chrome_options)

        # Clear cookies
        self.browser.delete_all_cookies()
        
        url = "https://nxbrew.com/search/{0}/".format(toSearch)
        self.log.info("Searching in: {0}".format(url))
        # Proxy tunnel the request
        if self.preferences.data["useProxy"] == 1:
            self.Proxy(url, False)
        else:
            # Access NxBrew.com directly without hide.me
            self.browser.get(url)
            self.scrape(self.browser.page_source)

    def listIcons(self) -> Tuple[list, list]:
        """"Get all icons links"""
        iconsLinks = []
        sizes = []
        icons = self.browser.find_elements_by_class_name("post-thumbnail")
        for icon in icons:
            # This are the links that need to be passed to the GUI for icon replacement
            height = int(icon.find_element_by_xpath(".//*/img").get_attribute("naturalHeight"))
            width = int(icon.find_element_by_xpath(".//*/img").get_attribute("naturalWidth"))
            sizes.append((height, width))
            iconsLinks.append(icon.find_element_by_xpath(".//*/img").get_attribute("src"))

        return iconsLinks, sizes

    def listGames(self) -> Tuple[list, list]:
        """Send all results found, after the search, to the GUI"""
        links = []
        # Index all results of the search specified in url -> toSearch
        posts = self.browser.find_elements_by_class_name("post-title")
        if not posts:
            if (self.browser.current_url == "https://nl.hideproxy.me/index.php"):
                self.log.warning("LOOPBACK TO HIDE.ME")
                return 1

        for post in posts:
            # This are the links that need to be passed to the browser for scrape()
            links.append(post.find_element_by_xpath(".//*").get_attribute("href"))

        # Check for no results
        if len(links) == 0:
            self.log.warning("NO RESULTS FOUND")
            return 0
        
        # Return all results found during search to the GUI
        # infos [0] = v.text
        # infos [1] = links
        infos = [],[]
        # Populate infos tuple
        for post in posts: infos[0].append(post.text)
        for link in links: infos[1].append(link)

        return infos

    def buildLink(self, link: str) -> str:
        # Find https: as starting point and & as the ending point, replace everything else correctly
        start = link.find("https%3A")
        end = link.find("&")
        link = link[start:end]
        link = link.replace("%3A", ":")
        link = link.replace("%2F", "/")
        return link

    def listLinks(self, link: str) -> Tuple[list, list]:
        """Get download links"""
        # Reset proxy connection if useProxy is enabled
        if self.preferences.data["useProxy"] == 1:
            downloadLinks = self.Proxy(self.buildLink(link), True)
        else:
            self.browser.get(link)
            downloadLinks = self.scrape(self.browser.page_source)

        return downloadLinks

    def cropImage(self, pathToImage: str, size: Tuple[int, int]) -> None:
        # Selenium screenshots the screen at a default resolution of 800x600
        # Size is a tuple containing height and width
        # ((800 - width)/2, (600 - height)/2) = top-left corner of icon
        # top-left + width & height = Icon
        """Grabs the game icon, removes the black borders"""
        boxArt = ((800-size[1])/2,(600-size[0])/2, (800-size[1])/2 + size[1], (600-size[0])/2 + size[0])
        img = Image.open(pathToImage, mode="r")
        cropped = img.crop(boxArt)
        os.remove(pathToImage)
        try:
            cropped.save(pathToImage)
        except SystemError as e:
            self.log.warning("Unable to crop image: {0}".format(e))
            print("Error: " + e)