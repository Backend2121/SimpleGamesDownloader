from typing import Any
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class searchGamesWorker(QThread):
    """First thread called, provides the games page from the search"""
    done = pyqtSignal(list)
    def __init__(self, module, text: str):
        super().__init__()
        self.module = module
        self.searchText = text
    def run(self):
        self.module.searchGame(self.searchText)
        returnValue = [self.module]
        self.done.emit(returnValue)