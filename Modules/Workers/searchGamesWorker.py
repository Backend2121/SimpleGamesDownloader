from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class searchGamesWorker(QThread):
    """First thread called, provides the games page from the search"""
    def __init__(self, sgd, text):
        super().__init__()
        self.sgd = sgd
        self.searchText = text
    def run(self):
        self.sgd.searchGame(self.searchText)
        return