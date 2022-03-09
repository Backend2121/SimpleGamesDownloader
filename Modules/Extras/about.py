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
        self.widget.setWindowIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Switch.png")))

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

        self.youtubeButton = QPushButton(" Youtube")
        self.youtubeButton.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Youtube.png")))
        self.youtubeButton.setIconSize(QSize(20,20))

        # BTC Address & Icon
        self.BTCAddress = QLabel()
        self.BTCAddress.setAlignment(Qt.AlignCenter)
        self.BTCAddress.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/Icons/BTCAddress.png")).scaled(128, 128, Qt.KeepAspectRatio))

        self.BTCIcon = QLabel()
        self.BTCIcon.setAlignment(Qt.AlignCenter)
        self.BTCIcon.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/Icons/BTC.png")).scaled(32, 32, Qt.KeepAspectRatio))

        self.BTCLabel = QLabel()
        self.BTCLabel.setText("bc1q0fuppgceyqlzhs9y4qyztqwaw40chd0rwlxf3q")
        self.BTCLabel.setAlignment(Qt.AlignCenter)
        self.BTCLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.BTCLayout = QVBoxLayout()
        self.BTCLayout.addWidget(self.BTCIcon)
        self.BTCLayout.addWidget(self.BTCAddress)
        self.BTCLayout.addWidget(self.BTCLabel)

        # ETH Address
        self.ETHAddress = QLabel()
        self.ETHAddress.setAlignment(Qt.AlignCenter)
        self.ETHAddress.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/Icons/ETHAddress.png")).scaled(128, 128, Qt.KeepAspectRatio))

        self.ETHIcon = QLabel()
        self.ETHIcon.setAlignment(Qt.AlignCenter)
        self.ETHIcon.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/Icons/ETH.png")).scaled(32, 32, Qt.KeepAspectRatio))

        self.ETHLabel = QLabel()
        self.ETHLabel.setText("0x04093b7d2B0698d3C3e61eC48702C070048614b7")
        self.ETHLabel.setAlignment(Qt.AlignCenter)
        self.ETHLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.ETHLayout = QVBoxLayout()
        self.ETHLayout.addWidget(self.ETHIcon)
        self.ETHLayout.addWidget(self.ETHAddress)
        self.ETHLayout.addWidget(self.ETHLabel)

        # Wallets layout
        self.walletLayout = QHBoxLayout()
        self.walletLayout.addLayout(self.BTCLayout)
        self.walletLayout.addLayout(self.ETHLayout)

        # Add to mainLayout
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.versionLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.discordButton)
        self.mainLayout.addWidget(self.redditButton)
        self.mainLayout.addWidget(self.patreonButton)
        self.mainLayout.addWidget(self.youtubeButton)
        self.mainLayout.addLayout(self.walletLayout)

        # Set main Layout
        self.widget.setLayout(self.mainLayout)

        # Set style.css
        self.widget.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.generalData["theme"] + ".css")).read())

        #Listeners
        self.discordButton.clicked.connect(self.openBrowserDiscord)
        self.redditButton.clicked.connect(self.openBrowserReddit)
        self.patreonButton.clicked.connect(self.openBrowserPatreon)
        self.youtubeButton.clicked.connect(self.openBrowserYoutube)

        # Show window
        self.widget.show()

    def openBrowserDiscord(self):
        webbrowser.open("https://discord.gg/WTrCtvyPke")

    def openBrowserReddit(self):
        webbrowser.open("https://www.reddit.com/user/Sbigioduro")
    
    def openBrowserPatreon(self):
        webbrowser.open("https://www.patreon.com/Backend2121")
    
    def openBrowserYoutube(self):
        webbrowser.open("https://www.youtube.com/channel/UCW2JQJs_R3O_I937yxicT9A")