from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import webbrowser
import json
import os

class About(QWindow):
    def __init__(self):
        super().__init__()
        # Load json for style.css
        with open("config.json",) as f:
            self.generalData = json.load(f)["General"]
            print(self.generalData)
            f.close()

        with open("version.json",) as f:
            self.version = json.load(f)
            f.close()
        
        # Main Layout
        self.mainLayout = QVBoxLayout()

        # Main Widget & modal
        self.widget = QWidget()
        self.widget.setWindowModality(Qt.ApplicationModal)
        self.widget.resize(600,200)
        self.widget.setWindowTitle("About")
        # Icon of widget
        self.widget.setWindowIcon(QIcon("Icons\\Switch.png"))

        # Labels
        self.titleLabel = QLabel("SGD")
        self.versionLabel = QLabel("Version: " + self.version["version"])
        self.descriptionLabel = QLabel("Modules update!")
        
        # PushButtons
        self.discordButton = QPushButton(" Discord")
        self.discordButton.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Discord.png")))
        self.discordButton.setIconSize(QSize(20,20))

        self.redditButton = QPushButton(" Reddit")
        self.redditButton.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Reddit.png")))
        self.redditButton.setIconSize(QSize(20,20))

        self.patreonButton = QPushButton(" Patreon")
        self.patreonButton.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Patreon.png")))
        self.patreonButton.setIconSize(QSize(20,20))

        # Add to mainLayout
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.versionLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.discordButton)
        self.mainLayout.addWidget(self.redditButton)
        self.mainLayout.addWidget(self.patreonButton)

        # Set main Layout
        self.widget.setLayout(self.mainLayout)

        # Set style.css
        self.widget.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.generalData["theme"] + ".css")).read())

        #Listeners
        self.discordButton.clicked.connect(self.openBrowserDiscord)
        self.redditButton.clicked.connect(self.openBrowserReddit)
        self.patreonButton.clicked.connect(self.openBrowserPatreon)
        # Show window
        self.widget.show()

    def openBrowserDiscord(self):
        webbrowser.open("https://discord.gg/WTrCtvyPke")

    def openBrowserReddit(self):
        webbrowser.open("https://www.reddit.com/user/Sbigioduro")
    
    def openBrowserPatreon(self):
        webbrowser.open("https://www.patreon.com/Backend2121")