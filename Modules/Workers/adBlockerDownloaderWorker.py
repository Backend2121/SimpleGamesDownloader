from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

# Install Requests if not found
try:
    import requests
except ModuleNotFoundError:
    os.system("pip install requests")
    import requests


class adBlockerDownloaderWorker(QThread):
    """First thread called, provides the games page from the search"""
    done = pyqtSignal(int)
    updated = pyqtSignal(int)
    def __init__(self):
        super().__init__()
    def run(self):
        r = requests.get('https://clients2.google.com/service/update2/crx?response=redirect&prodversion=92.0.4515.131&acceptformat=crx2,crx3&x=id%3Dcfhdojbkjhnklbpkdaibdccddilifddb%26uc')
        dl = 0
        # Hardcoded but should remain constant in the future
        total_length = 2254
        
        with open(os.getcwd() + "\\Modules\\adblock.crx", "wb") as f:
            for data in r.iter_content(chunk_size=512):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                self.updated.emit(done*2)
            f.close()
        self.done.emit(1)