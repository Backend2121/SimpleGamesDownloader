from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import webbrowser
import json

class About(QWindow):
    def __init__(self):
        super().__init__()
        # Load json for style.css
        with open("config.json",) as f:
            self.data = json.load(f)
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
        self.titleLabel = QLabel("Switch Games Downloader")
        self.versionLabel = QLabel("Version: " + self.version["version"])
        self.descriptionLabel = QLabel("Now with a GUI!")
        
        # PushButtons
        self.discordButton = QPushButton(" Discord")
        self.discordButton.setIcon(QIcon("Icons\\Discord.png"))
        self.discordButton.setIconSize(QSize(20,20))

        self.redditButton = QPushButton(" Reddit")
        self.redditButton.setIcon(QIcon("Icons\\Reddit.png"))
        self.redditButton.setIconSize(QSize(20,20))

        # Add to mainLayout
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.versionLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.discordButton)
        self.mainLayout.addWidget(self.redditButton)

        # Set main Layout
        self.widget.setLayout(self.mainLayout)

        # Set style.css
        self.widget.setStyleSheet(open("Themes\\" + self.data["theme"] + ".css", "r").read())

        #Listeners
        self.discordButton.clicked.connect(self.openBrowserDiscord)
        self.redditButton.clicked.connect(self.openBrowserReddit)
        # Show window
        self.widget.show()

    def openBrowserDiscord(self):
        webbrowser.open("https://discord.gg/WTrCtvyPke")

    def openBrowserReddit(self):
        webbrowser.open("https://www.reddit.com/user/Sbigioduro")