from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Modules.Extras.manualCaptcha import browser

class manualCaptchaWorker(QThread):
    """Captcha thread called, provides an instance of Chrome to manually solve the Captcha"""
    done = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.b = browser()

    def run(self):
        self.done.emit(self.b.start(self.link))
    
    def setLink(self, link):
        self.link = link