from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class cleanLinkWorker(QThread):
    done = pyqtSignal(str)
    def __init__(self, module, text: str):
        super().__init__()
        self.module = module
        self.link = text
    def run(self):
        self.done.emit(self.module.cleanLink(self.link))