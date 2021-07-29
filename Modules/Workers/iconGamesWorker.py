from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class iconGamesWorker(QThread):
    """Third thread called, provides the icons for the games listed"""
    done = pyqtSignal(tuple)
    def __init__(self, sgd):
        super().__init__()
        self.sgd = sgd
        
    def run(self):
        self.done.emit(self.sgd.listIcons())