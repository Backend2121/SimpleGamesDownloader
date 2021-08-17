from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class cleanLinkWorker(QThread):
    """First thread called, provides the games page from the search"""
    done = pyqtSignal(str)
    def __init__(self, sgd, text):
        super().__init__()
        self.sgd = sgd
        self.link = text
    def run(self):
        self.done.emit(self.sgd.CleanLink(self.link))