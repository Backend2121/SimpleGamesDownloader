import os

# Check if pip exists if not install
if (os.system("pip -V") != 0):
    os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    os.system("python get-pip.py")
    os.remove("get-pip.py")

# Install PyQt5 if not found
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ModuleNotFoundError:
    os.system("pip install PyQt5")
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

from Modules.about import About
from Modules.preferences import Preferences
from Modules.SGD import SGD
from Modules.Workers.searchGamesWorker import searchGamesWorker
from Modules.Workers.listGamesWorker import listGamesWorker
from Modules.Workers.iconGamesWorker import iconGamesWorker
from Modules.Workers.listLinksWorker import listLinksWorker
from Modules.Workers.cleanLinkWorker import cleanLinkWorker
from Modules.Workers.manualCaptchaWorker import manualCaptchaWorker
import webbrowser
import random

class App():
    def __init__(self, main):
        if main:
            # Main App definitions
            self.app = QApplication([])
            self.window = QMainWindow()
            self.widget = QWidget()
            self.properties = Preferences()
            self.createLayout()
            self.setWindowParameters()
            self.createWidgets()
            self.widget.show()
            self.checkUpdates()
            self.checkChromeDriver()
            self.app.exec_()

    def alarm(self, title, label):
        """Used to deliver info/errors to the user (str, str)"""
        message = QMessageBox()
        # Set style
        message.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())
        # Display message
        message.about(self.widget, title, label)

    def updateAvailable(self, title, label):
        """Create a pop-up widget used to copy informations"""

        # Create QMessageBox and set text and title
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(label)
        # Icon of widget
        message.setWindowIcon(QIcon("Icons\\Switch.png"))

        # Set style
        message.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())

        # Create buttons
        browser = QPushButton(' Open')
        browser.setIcon(QIcon("Icons\\Github.png"))

        # Assign buttons to QMessageBox
        message.addButton(browser, QMessageBox.YesRole)

        # Listener
        browser.clicked.connect(self.openGithub)

        # Execute
        message.exec_()

    def chromeDriverNotFound(self, title, label):
        """Create a pop-up widget used to notify the user"""

        # Create QMessageBox and set text and title
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(label)
        # Icon of widget
        message.setWindowIcon(QIcon("Icons\\Switch.png"))

        # Set style
        message.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())

        # Create buttons
        download = QPushButton(' Download')
        close = QPushButton(' Close')
        download.setIcon(QIcon("Icons\\DownloadIcon.png")) #REPLACE WITH DOWNLOAD ICON

        # Assign buttons to QMessageBox
        message.addButton(close, QMessageBox.NoRole)
        message.addButton(download, QMessageBox.YesRole)

        # Listeners
        download.clicked.connect(self.startCDDownload)

        # Execute
        message.exec_()

    def startCDDownload(self):
        # Import ChromeDriver downloader
        from Modules.chromedriverGetter import worker
        message = QMessageBox()
        layout = message.layout()
        message.setWindowTitle("Downloading...")

        # Define widgets
        self.pbar = QProgressBar()
        label = QLabel("Getting the ChromeDriver for you <3!")

        # Add to layout
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.pbar, 1, 0)

        # Icon of widget
        message.setWindowIcon(QIcon("Icons\\Switch.png"))

        # Set style
        message.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())
        self.close = QPushButton(' Close')
        message.addButton(self.close, QMessageBox.YesRole)
        self.close.setEnabled(False)
        # Start downloader thread
        downloader = worker()
        downloader.updated.connect(self.updatePBar)
        downloader.start()

        # Start window
        message.exec_()

    def updatePBar(self, value):
        self.pbar.setValue(value)
        if (value >= 99):
            self.close.setEnabled(True)

    def openGithub(self):
        """Open latest release on GitHub"""
        webbrowser.open("https://github.com/Backend2121/SwitchGamesDownloader/releases/latest")

    def checkUpdates(self):
        version = os.popen("curl https://github.com/Backend2121/SwitchGamesDownloader/releases/latest").read()
        urlStart = version.find("/tag/")
        urlEnd = version.find('">')
        if version[urlStart+5:urlEnd] == self.properties.version["version"]:
            pass
        else:
            self.updateAvailable("Update found", "A new version of this software is available on GitHub!")
    
    def checkChromeDriver(self):
        if os.path.isfile("chromedriver.exe"):
            return
        else:
            self.chromeDriverNotFound("ChromeDriver not found!", "Do you want to download the ChromeDriver?")

    def linkPopUp(self, title, label):
        """Create a pop-up widget used to copy informations"""
        
        # Create QMessageBox and set text and title
        self.message = QMessageBox()
        self.message.setWindowTitle(title)
        self.message.setText(label)

        # Set style
        self.message.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())

        # Create buttons
        copy = QPushButton('Copy')
        browser = QPushButton('Open')

        # Assign buttons to QMessageBox
        self.message.addButton(copy, QMessageBox.YesRole)
        self.message.addButton(browser, QMessageBox.YesRole)

        # Listeners
        copy.clicked.connect(self.copy)
        browser.clicked.connect(self.browser)

        # Reset output box
        self.resultBox.setText(self.greetings())
        self.resultBox.movie = None

        # Execute
        self.message.exec_()

    def copy(self):
        """Copy shown link"""
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.message.text(), mode=cb.Clipboard)

    def browser(self):
        """Open shown link in a browser"""
        webbrowser.open(self.message.text())

    def directBrowser(self, text):
        """Open link passed in as argument"""
        self.resultBox.setText(self.greetings())
        self.resultBox.movie = None
        webbrowser.open(text)

    def greetings(self):
        greets = ["Hi!", "Hello there!", "Hey!", "Honk!", "Whassup!", "I promise i won't hang", "What do you need?", "Here to help!", "How are you doing?", "Join the Discord!", "SGD has a Patreon!"]
        return greets[random.randrange(0,len(greets))]

    def DownloadIcon(self):
        for k,icon in enumerate(self.icons):
            # Download image
            self.sgd.browser.get(icon)
            self.sgd.browser.save_screenshot("GameIcons\\" + str(k) + ".png")
            # Resize image
            self.sgd.cropImage("GameIcons\\" + str(k) + ".png", self.sizes[k])

    def search(self):
        # Clear any previous garbage
        self.listWidget.clear()
        self.linksListWidget.clear()

        # Instantiate universal SGD class
        try:
            if self.sgd in locals(): pass
        except:
            self.sgd = SGD()

        # Create and start searchGamesWorker thread
        self.searchWorker = searchGamesWorker(self.sgd, self.searchBox.text())
        self.searchWorker.start()
        self.searchWorker.finished.connect(self.populateSearchList)
        self.searchButton.setEnabled(False)
        self.movieLoading = QMovie("Icons\\Loading.gif")
        self.movieLoading.setScaledSize(QSize(self.properties.data["UIIconSizePx"] * 2, self.properties.data["UIIconSizePx"] * 2))
        self.resultBox.setMovie(self.movieLoading)
        self.movieLoading.start()

    def displayLinks(self, value):
        tupleElement = value
        for k,v in enumerate(tupleElement[0]):
            # Entries
            if tupleElement[1][k] != "- ":
                item = QListWidgetItem(tupleElement[1][k] + " " + v)
                if self.properties.data["theme"] == "Dark":
                    item.setForeground(QColor("green"))
                if self.properties.data["theme"] == "Aqua":
                    item.setForeground(QColor("green"))
                if self.properties.data["theme"] == "Light":
                    item.setForeground(QColor("blue"))
                if self.properties.data["theme"] == "Patriotic":
                    item.setForeground(QColor("white"))
            # Links
            else:
                item = QListWidgetItem("- " + v)
                if self.properties.data["theme"] == "Dark":
                    item.setForeground(QColor("white"))
                if self.properties.data["theme"] == "Aqua":
                    item.setForeground(QColor("white"))
                if self.properties.data["theme"] == "Light":
                    item.setForeground(QColor("black"))
                if self.properties.data["theme"] == "Patriotic":
                    item.setForeground(QColor("green"))
            # Printing links on the rightside box
            self.linksListWidget.addItem(item)
        self.resultBox.setText(self.greetings())
        self.resultBox.movie = None

    def selectGame(self):
        """Once game is selected, links will be provided on the right side box"""
        self.linksListWidget.clear()

        # Make resume
        self.resumeIcon.setPixmap(QPixmap("GameIcons\\" + str(self.listWidget.currentRow()) + ".png").scaled(self.properties.data["GameIconSizePx"] * 2,self.properties.data["GameIconSizePx"] * 2, Qt.KeepAspectRatio))
        self.resumeLabel.setText(self.infos[0][self.listWidget.currentRow()])
        self.resumeLabel.setFont(QFont("Arial", self.properties.data["resumefont"]))
        self.resumeLayout.addWidget(self.resumeIcon)
        self.resumeLayout.addWidget(self.resumeLabel)

        # Save the tuple element returned from listLinks
        # Create and start listLinksWorker thread
        self.linksWorker = listLinksWorker(self.sgd, self.infos[1][0][self.listWidget.currentRow()])
        self.linksWorker.start()
        self.linksWorker.done.connect(self.displayLinks)
        self.movieLoading = QMovie("Icons\\Loading.gif")
        self.movieLoading.setScaledSize(QSize(self.properties.data["UIIconSizePx"] * 2, self.properties.data["UIIconSizePx"] * 2))
        self.resultBox.setMovie(self.movieLoading)
        self.movieLoading.start()

    def outputLink(self, link):
        # Ads skipping and stuff inside SGD.py
        # Re-enable links list
        self.linksListWidget.setDisabled(False)
        if "http" in link:
            # If openLinks in config.json is set to 1/True, open the link in the browser
            if self.properties.data["openLinks"] == 1 and self.properties.data["semiAutoMode"] == 0:
                self.directBrowser(link)

            # Semi-Automatic mode preference
            elif self.properties.data["semiAutoMode"] == 1:
                self.captchaWorker = manualCaptchaWorker()
                self.captchaWorker.setLink(link)
                self.captchaWorker.start()
                self.captchaWorker.done.connect(self.provideFinalLink)

            # Ask the user to copy/open the link
            elif self.properties.data["openLinks"] == 0:
                self.linkPopUp("Success!", link)

        else:
            self.resultBox.setText("Error: The entry you choose is not a link!")

    def provideFinalLink(self, link):
        if link == "closed":
            self.resultBox.setText("Error: Closed")
            return
        if self.properties.data["openLinks"] == 1:
            if "magnet" not in link:
                self.directBrowser(link)
            else:
                self.linkPopUp("Success!", link)
        else:
            self.linkPopUp("Success!", link)

    def fetchDownloadLink(self):
        self.movieLoading = QMovie("Icons\\Loading.gif")
        self.movieLoading.setScaledSize(QSize(self.properties.data["UIIconSizePx"] * 2, self.properties.data["UIIconSizePx"] * 2))
        self.resultBox.setMovie(self.movieLoading)
        self.movieLoading.start()
        try:
            # Create and start cleanLinkWorker thread
            self.cleanWorker = cleanLinkWorker(self.sgd, self.linksListWidget.selectedItems()[0].text())
            self.cleanWorker.start()
            self.cleanWorker.done.connect(self.outputLink)
            # Disable links list
            self.linksListWidget.setDisabled(True)
        except:
            pass

    def setWindowParameters(self):
        # Title of main widget
        self.widget.setWindowTitle("SwitchGamesDownloader")

        # Icon of main widget
        self.widget.setWindowIcon(QIcon("Icons\\Switch.png"))

        # Default size of GUI
        self.widget.resize(self.properties.data["Width"], self.properties.data["Height"])

        # Theme
        self.widget.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())

    def createList(self, value):
        self.icons = value[0]
        self.sizes = value[1]
        self.DownloadIcon()
        try:
            if self.properties.data["loadicons"] == 1:
                for k,v in enumerate(self.infos[0]):
                    self.listWidget.addItem(QListWidgetItem(QIcon("GameIcons\\" + str(k) + ".png"), str(v)))
            else:
                for k,v in enumerate(self.infos[0]):
                    self.listWidget.addItem(QListWidgetItem(QIcon("GameIcons\\default.png"), str(v)))
        except TypeError as e:
            print(e)
            # No results found error
            self.alarm("Error", "No results found!")
        self.listWidget.setIconSize(QSize((self.properties.data["GameIconSizePx"]), (self.properties.data["GameIconSizePx"])))
        self.resultBox.setText(self.greetings())
        self.resultBox.movie = None

    def makeInfos(self, value):
        self.infos = value
        if self.infos == 1:
            self.search()
        if self.properties.data["loadicons"] == 1:
            # Create and start listIconsWorker thread
            self.iconWorker = iconGamesWorker(self.sgd)
            self.iconWorker.start()
            self.iconWorker.done.connect(self.createList)

    def populateSearchList(self):
        # This will be populated by search results with icons and game title
        self.listWidget.clear()
        self.linksListWidget.clear()
        self.resumeIcon.setPixmap(QPixmap("GameIcons\\default.png").scaled(self.properties.data["GameIconSizePx"] * 2,self.properties.data["GameIconSizePx"] * 2, Qt.KeepAspectRatio))
        self.resumeLabel.clear()
        # Create and start listGamesWorker thread
        self.gamesWorker = listGamesWorker(self.sgd)
        self.gamesWorker.start()
        self.gamesWorker.done.connect(self.makeInfos)
        self.searchButton.setEnabled(True)

    def createLayout(self):
        # Create general layout
        self.mainLayout = QHBoxLayout()

        # SubLayouts
        self.listLayout = QVBoxLayout()
        self.searchFunctionLayout = QHBoxLayout()
        self.searchLayout = QVBoxLayout()
        self.resumeLayout = QHBoxLayout()
        self.searchLayout.addLayout(self.searchFunctionLayout)
        self.searchLayout.addLayout(self.resumeLayout)
        # Add to mainLayout
        self.mainLayout.addLayout(self.listLayout)
        self.mainLayout.addLayout(self.searchLayout)

    def closeWindow(self):
        exit()

    def preferencesWindow(self):
        self.p = Preferences()
        self.p.widget.exec_()
        self.properties.data = self.p.data
        self.updatePreferences()

    def aboutWindow(self):
        self.a = About()

    def updatePreferences(self):
        self.listWidget.setIconSize(QSize((self.properties.data["GameIconSizePx"]), (self.properties.data["GameIconSizePx"])))
        self.searchButton.setIconSize(QSize((self.properties.data["UIIconSizePx"]), (self.properties.data["UIIconSizePx"])))
        self.widget.resize(self.properties.data["Width"], self.properties.data["Height"])
        self.widget.setStyleSheet(open("Themes\\" + self.properties.data["theme"] + ".css", "r").read())

    def createWidgets(self):
        # Widget creation
        self.listWidget = QListWidget()

        # Top menu bar
        self.menu = QMenuBar()
        self.listLayout.addWidget(self.menu)

        # Options for menubar
        self.file = self.menu.addMenu("File")
        self.options = self.menu.addMenu("Options")
        self.about = self.menu.addMenu("About")

        # Quit Action
        self.quit = QAction("Quit", self.file)
        self.quit.setShortcut("Ctrl+Q")

        # Options Action
        self.preferencesMenu = QAction("Preferences", self.options)
        self.preferencesMenu.setShortcut("Ctrl+P")

        # About Action
        self.aboutMenu = QAction("Info", self.about)
        self.aboutMenu.setShortcut("Ctrl+H")

        # Add to menu
        self.file.addAction(self.quit)
        self.options.addAction(self.preferencesMenu)
        self.about.addAction(self.aboutMenu)

        # SearchBar
        self.searchBar = QFormLayout()

        #Create textBox for user input
        self.searchBox = QLineEdit()
        self.searchBar.addRow("Game Search: ", self.searchBox)
        self.searchFunctionLayout.addLayout(self.searchBar)

        # Search Button
        self.searchButton = QPushButton()
        self.searchButton.setIcon(QIcon("Icons\\WebScraping.png"))
        self.searchButton.setIconSize(QSize((self.properties.data["UIIconSizePx"]), (self.properties.data["UIIconSizePx"])))
        self.searchButton.setShortcut("Return")
        self.searchFunctionLayout.addWidget(self.searchButton)

        # Resume widget
        self.resumeIcon = QLabel()
        self.resumeLabel = QLabel()
        self.resumeIcon.setPixmap(QPixmap("GameIcons\\default.png").scaled(self.properties.data["GameIconSizePx"] * 2,self.properties.data["GameIconSizePx"] * 2, Qt.KeepAspectRatio))
        self.resumeLayout.addWidget(self.resumeIcon)
        self.resumeLayout.addWidget(self.resumeLabel)

        # Final Output Box
        self.resultBox = QLabel()

        # Add random greetings
        self.resultBox.setText(self.greetings())

        # Bottom-right list with all download links
        self.linksListWidget = QListWidget()
        self.searchLayout.addWidget(self.linksListWidget)
        self.searchLayout.addWidget(self.resultBox)

        # Add listWidget to the main layout
        self.listLayout.addWidget(self.listWidget)

        # Set the widget's main layout to layout
        self.widget.setLayout(self.mainLayout)

        # LISTENERS
        # Assign the button a function with a listener
        self.searchButton.clicked.connect(self.search)
        # Assign the listWidget a function OnValueChanged with a listener
        self.listWidget.itemSelectionChanged.connect(self.selectGame)
        self.linksListWidget.itemSelectionChanged.connect(self.fetchDownloadLink)
        self.quit.triggered.connect(self.closeWindow)
        self.preferencesMenu.triggered.connect(self.preferencesWindow)
        self.about.triggered.connect(self.aboutWindow)

if __name__ == "__main__":
    App(True)
