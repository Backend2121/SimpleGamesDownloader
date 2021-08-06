from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Modules.adBlockerDownloader import downloadAdBlocker

class adBlockerDownloaderWorker(QThread):
    """First thread called, provides the games page from the search"""
    done = pyqtSignal(int)
    def __init__(self):
        super().__init__()
    def run(self):
        downloadAdBlocker()
        self.done.emit(1)