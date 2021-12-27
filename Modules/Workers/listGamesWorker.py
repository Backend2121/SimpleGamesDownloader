from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class listGamesWorker(QThread):
    """Second thread called, provides the list of games from the searched page"""
    done = pyqtSignal(list)
    def __init__(self, module):
        super().__init__()
        self.module = module
        
    def run(self):
        self.done.emit([self.module.listGames(), self.module])