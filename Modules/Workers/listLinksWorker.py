from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class listLinksWorker(QThread):
    """Forth thread called, provides the download links for the searched game as well as a represetative string"""
    done = pyqtSignal(tuple)
    def __init__(self, module, link: str):
        super().__init__()
        self.module = module
        self.link = link

    def run(self):
        self.done.emit(self.module.listLinks(self.link))