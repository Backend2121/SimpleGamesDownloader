from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class iconGamesWorker(QThread):
    """Third thread called, provides the icons for the games listed"""
    done = pyqtSignal(list)
    def __init__(self, module):
        super().__init__()
        self.module = module
        
    def run(self):
        self.done.emit([self.module.listIcons(), self.module])