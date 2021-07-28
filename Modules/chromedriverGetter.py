import os
import requests
from bs4 import BeautifulSoup
import zipfile
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def getVersion():
    version = os.popen('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
    version = version.replace(" ", "")
    start = version.find("REG_SZ")
    version = version.replace("REG_SZ", "")
    end = version.rfind(".")
    
    return version[start:end]

def getCD(pbar):
    """Threaded function that downloads the correct version of ChromeDriver"""
    version = getVersion()
    pbar.setValue(10)
    # Get raw html of chromedriver's page to give to bs4 for scraping
    r = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + version)
    soup = BeautifulSoup(r.content, 'html.parser')
    print("curl https://chromedriver.storage.googleapis.com/index.html?path="+ soup.text +"/chromedriver_win32.zip -o ChromeDriver.exe")
    os.system("curl https://chromedriver.storage.googleapis.com/"+ soup.text +"/chromedriver_win32.zip -o ChromeDriver.zip")
    with zipfile.ZipFile("ChromeDriver.zip", 'r') as zip_ref:
        zip_ref.extractall(".")
    os.remove("ChromeDriver.zip")