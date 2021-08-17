from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class listGamesWorker(QThread):
    """Second thread called, provides the list of games from the searched page"""
    done = pyqtSignal(tuple)
    def __init__(self, sgd):
        super().__init__()
        self.sgd = sgd
        
    def run(self):
        self.done.emit(self.sgd.listGames())