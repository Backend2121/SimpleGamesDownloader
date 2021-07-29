from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class listLinksWorker(QThread):
    """Forth thread called, provides the download links for the searched game"""
    done = pyqtSignal(tuple)
    def __init__(self, sgd, link):
        super().__init__()
        self.sgd = sgd
        self.link = link

    def run(self):
        self.done.emit(self.sgd.listLinks(self.link))