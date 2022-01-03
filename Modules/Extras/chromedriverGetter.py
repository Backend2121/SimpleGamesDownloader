import os
import logging
import requests

from bs4 import BeautifulSoup
import zipfile
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class worker(QThread):
    updated = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.logPath = os.path.normpath(os.getcwd() + "//ReplaceWithTime.log")
        self.log = logging.getLogger("NXBrew_Logger")
        logging.basicConfig(filename=self.logPath , filemode='a', format='%(levelname)s - %(name)s - "%(asctime)s": %(message)s', level="INFO")

    def getVersion(self) -> str:
        version = os.popen('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
        version = version.replace(" ", "")
        start = version.find("REG_SZ")
        version = version.replace("REG_SZ", "")
        end = version.rfind(".")
        self.log.info("Chromedriver version needed: {0}".format(version[start:end]))
        
        return version[start:end]

    def run(self) -> None:
        """Threaded function that downloads the correct version of ChromeDriver"""
        version = self.getVersion()
        # Get raw html of chromedriver's page to give to bs4 for scraping
        r = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + version)
        soup = BeautifulSoup(r.content, 'html.parser')
        # Code "stolen" from https://stackoverflow.com/a/15645088
        r = requests.get("https://chromedriver.storage.googleapis.com/"+ soup.text +"/chromedriver_win32.zip", stream=True)
        total_length = r.headers.get('content-length')
        self.log.info("Chromedriver total size: {0}".format(total_length))
        dl = 0
        total_length = int(total_length)
        with open("ChromeDriver.zip", "wb") as f:
            for data in r.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                self.updated.emit(done*2)
            f.close()
        self.log.info("Chromedriver download complete")
        # Extract and delete ChromeDriver.zip
        try:
            with zipfile.ZipFile("ChromeDriver.zip", 'r') as zip_ref:
                zip_ref.extractall(str(os.getcwd()))
                self.log.info("Extraction of ChromeDriver.zip complete")
        except Exception as e:
            self.log.info("An error occurred during the extraction of ChromeDriver.exe: {0}", e)
        os.remove("ChromeDriver.zip")