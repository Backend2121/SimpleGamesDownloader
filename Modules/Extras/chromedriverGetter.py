import os

# Install Requests if not found
try:
    import requests
except ModuleNotFoundError:
    os.system("pip install requests")
    import requests

from bs4 import BeautifulSoup
import zipfile
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class worker(QThread):
    updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def getVersion(self):
        version = os.popen('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
        version = version.replace(" ", "")
        start = version.find("REG_SZ")
        version = version.replace("REG_SZ", "")
        end = version.rfind(".")
        
        return version[start:end]

    def run(self):
        """Threaded function that downloads the correct version of ChromeDriver"""
        version = self.getVersion()
        # Get raw html of chromedriver's page to give to bs4 for scraping
        r = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + version)
        soup = BeautifulSoup(r.content, 'html.parser')
        # Code "stolen" from https://stackoverflow.com/a/15645088
        r = requests.get("https://chromedriver.storage.googleapis.com/"+ soup.text +"/chromedriver_win32.zip", stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        total_length = int(total_length)
        with open("ChromeDriver.zip", "wb") as f:
            for data in r.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                self.updated.emit(done*2)
            f.close()
        # Extract and delete ChromeDriver.zip
        with zipfile.ZipFile("ChromeDriver.zip", 'r') as zip_ref:
            zip_ref.extractall(str(os.getcwd()))
        os.remove("ChromeDriver.zip")