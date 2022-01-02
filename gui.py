import os
import logging
import importlib
import time
import webbrowser
import random
import sys

# Check if pip exists if not install
if (os.system("pip -V") != 0):
    os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    os.system("python get-pip.py")
    os.remove("get-pip.py")

# Install all pre-requisites
os.system("pip install -r requirements.txt")

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Modules.Extras.about import About
from Modules.Extras.preferences import Preferences
from Modules.Workers.searchGamesWorker import searchGamesWorker
from Modules.Workers.listGamesWorker import listGamesWorker
from Modules.Workers.iconGamesWorker import iconGamesWorker
from Modules.Workers.listLinksWorker import listLinksWorker
from Modules.Workers.cleanLinkWorker import cleanLinkWorker

class App():
    def __init__(self, main: bool):
        if main:
            # Main App definitions
            self.app = QApplication([])
            self.window = QMainWindow()
            self.widget = QWidget()
            self.modulesSettings = []

            # Define logger
            
            self.log = logging.getLogger("MAIN_Logger")

            # Create Logs folder if not present
            if not (os.path.isdir(os.path.normpath(os.getcwd() + "//Logs"))):
                os.mkdir(os.path.normpath(os.getcwd() + "//Logs"))
            
            self.logPath = os.path.normpath(os.getcwd() + "//Logs//{0}.log".format(time.strftime("%Y%m%d-%H%M%S")))
            logging.basicConfig(filename=self.logPath , filemode='a', format='%(levelname)s - %(name)s - "%(asctime)s": %(message)s', level="INFO")

            # Get general info of the running machine
            self.log.info("PYTHON VERSION: {0}".format(sys.version))
            self.log.info("PLATFORM: {0}".format(sys.platform))

            # Import all modules in "Modules" folder
            for f in os.listdir(os.path.normpath(os.getcwd() + "/Modules")):
                if (".py" in f):
                    f = f.replace(".py", "")
                    imported = importlib.import_module("." + f, "Modules")
                    x = imported.Settings()
                    x.logPath = self.logPath
                    self.modulesSettings.append(imported.Settings())

            self.log.info("Loaded {0} module(s)".format(self.modulesSettings))
            self.properties = Preferences(self.modulesSettings)
            self.createLayout()
            self.setWindowParameters()
            self.createWidgets()
            self.widget.show()
            self.alarm("WARNING", "This software MUST ONLY be used to download LEGALLY BOUGHT GAMES to play them on emulators!\n\nI do not condone any form of piracy!")
            self.checkUpdates()
            self.checkChromeDriver()
            self.app.exec_()

# REGION Pop-up Boxes
    def alarm(self, title: str, label: str) -> None:
        """Used to deliver info/errors to the user"""
        message = QMessageBox()
        # Set style
        message.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())
        # Display message
        message.about(self.widget, title, label)

    def updateAvailable(self, title: str, label: str) -> None:
        """Create a pop-up widget used to copy informations"""

        # Create QMessageBox and set text and title
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(label)
        # Icon of widget
        message.setWindowIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Switch.png")))

        # Set style
        message.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())

        # Create buttons
        browser = QPushButton(' Open')
        browser.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Github.png")))

        # Assign buttons to QMessageBox
        message.addButton(browser, QMessageBox.YesRole)

        # Listener
        browser.clicked.connect(self.openGithub)

        # Execute
        message.exec_()# ENDREGION
# REGION ChromeDriver Downloader
    def chromeDriverNotFound(self, title: str, label: str) -> None:
        """Create a pop-up widget used to notify download the ChromeDriver"""

        # Create QMessageBox and set text and title
        message = QMessageBox()
        message.setWindowTitle(title)
        message.setText(label)
        # Icon of widget
        message.setWindowIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Switch.png")))

        # Set style
        message.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())

        # Create buttons
        download = QPushButton(' Download')
        close = QPushButton(' Close')
        download.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/DownloadIcon.png")))

        # Assign buttons to QMessageBox
        message.addButton(close, QMessageBox.NoRole)
        message.addButton(download, QMessageBox.YesRole)

        # Listeners
        download.clicked.connect(self.startCDDownload)

        # Execute
        message.exec_()

    def startCDDownload(self) -> None:
        """Doesn't work with Linux/MacOS"""
        # Import ChromeDriver downloader
        from Modules.Extras.chromedriverGetter import worker
        self.CDDialog = QMessageBox()
        layout = self.CDDialog.layout()
        self.CDDialog.setWindowTitle("Downloading...")

        # Define widgets
        self.pbar = QProgressBar()
        self.percent = QLabel()
        label = QLabel("Getting the ChromeDriver for you <3!")

        # Add to layout
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.pbar, 1, 0)
        # layout.addWidget(self.percent, 1, 1)

        # Icon of widget
        self.CDDialog.setWindowIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Switch.png")))

        # Set style
        self.CDDialog.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())
        self.close = QPushButton(' Close')
        self.CDDialog.addButton(self.close, QMessageBox.YesRole)
        self.close.setEnabled(False)
        # Start downloader thread
        self.prevValue = 0
        downloader = worker()
        downloader.logPath = self.logPath
        downloader.updated.connect(self.updatePBar)
        downloader.start()
        self.log.info("Chromedriver downloader worker started")

        # Start window
        self.CDDialog.exec_()
    
    def updatePBar(self, value: int) -> None:
        """Update progress bar using the value passed in (0-100)"""
        self.pbar.setValue(value)
        if self.prevValue != value:
            self.prevValue = value
            self.log.info("Download percentage: {0}".format(value))
        if (value >= 99):
            self.close.setEnabled(True)
            self.CDDialog.close()# ENDREGION
    def openGithub(self) -> None:
        """Open latest release on GitHub"""
        webbrowser.open("https://github.com/Backend2121/SwitchGamesDownloader/releases/latest")

    def checkUpdates(self) -> None:
        version = os.popen("curl https://github.com/Backend2121/SwitchGamesDownloader/releases/latest").read()
        urlStart = version.find("/tag/")
        urlEnd = version.find('">')
        if version[urlStart+5:urlEnd] == self.properties.version["version"]:
            pass
        else:
            self.updateAvailable("Update found", "A new version of this software is available on GitHub!")
    
    def checkChromeDriver(self) -> None:
        if os.path.isfile("chromedriver.exe"):
            return
        else:
            if sys.platform == "win32":
                self.log.info("Starting chromdriver downloader for {0}".format(sys.platform))
                self.chromeDriverNotFound("ChromeDriver not found!", "Do you want to download the ChromeDriver?")
            else:
                self.log.info("Unable to automatically download chromedriver for {0}".format(sys.platform))
                self.alarm("WARNING", "You do not have the chromedriver in the main directory of the script\nAutomatic download is not supported for Linux/MacOS\nYou must download it manually!")

    def linkPopUp(self, title: str, label: str) -> None:
        """Create a pop-up widget used to copy informations"""
        
        # Create QMessageBox and set text and title
        self.message = QMessageBox()
        self.message.setWindowTitle(title)
        self.message.setText(label)

        # Set style
        self.message.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())

        # Create buttons
        copy = QPushButton('Copy')
        browser = QPushButton('Open')
        # Button for the auto download (grayed by default)
        download = QPushButton('Download')

        # Assign buttons to QMessageBox
        self.message.addButton(copy, QMessageBox.YesRole)
        self.message.addButton(browser, QMessageBox.YesRole)
        self.message.addButton(download, QMessageBox.YesRole)

        # Listeners
        copy.clicked.connect(self.copy)
        browser.clicked.connect(self.browser)
        download.clicked.connect(self.downloadManager)

        # Reset output box
        self.resultBox.setText(self.greetings())
        self.movieBox.clear()

        # Execute
        self.message.exec_()
# REGION LinkPopUp buttons functions
    def copy(self) -> None:
        """Copy shown link"""
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.message.text(), mode=cb.Clipboard)

    def browser(self) -> None:
        """Open shown link in a browser"""
        self.log.info("Opening browser to {0}".format(self.message.text()))
        webbrowser.open(self.message.text())

    def downloadManager(self) -> None:
        """PLACEHOLDER"""
        print("PLACEHOLDER")# ENDREGION
# REGION MISC/FUN
    def greetings(self) -> str:
        greets = ["Hi!", "Hello there!", "Hey!", "Honk!", "Whassup!", "I promise i won't hang", "What do you need?", "Here to help!", "How are you doing?", "Join the Discord!", "Praise the Sun!", "For science, you monster", "It's dangerous to go alone, use me!", "Stupid Shinigami", "Trust me i'm a dolphin!", "...", "Oh, it's you...", "The cake is a lie!", "FBI open up!", "You own the game, right?"]
        return greets[random.randint(0, len(greets) - 1)]

    def directBrowser(self, text: str) -> None:
        """Open link passed in as argument"""
        self.resultBox.setText(self.greetings())
        self.movieBox.clear()
        webbrowser.open(text)# ENDREGION
# REGION Search Phase
    def DownloadIcon(self, module, name: str) -> None:
        """Downloads the games icons inside 'GameIcons' folder"""
        for k,icon in enumerate(self.icons):
            self.downloadCounter = self.downloadCounter + 1
            # Download image
            module.browser.get(icon)
            module.browser.save_screenshot(os.path.normpath(os.getcwd() + "/GameIcons/_" + name + "_" + str(self.downloadCounter) + ".png"))
            # Resize image
            # The try except is needed because the first image to be downloaded is corrupted for some reason
            try:
                module.cropImage(os.path.normpath(os.getcwd() + "/GameIcons/_" + name + "_" + str(self.downloadCounter) + ".png"), self.sizes[k])
            except:
                continue

    def lock(self, module):
        self.done.append(module)
        # Wait for all modules to complete the search
        if len(self.done) < self.pending:
            self.resultBox.setText("Completed search with " + str(len(self.done)) + "/" + str(self.pending) + " module(s)")
            self.log.info("Completed search with " + str(len(self.done)) + "/" + str(self.pending) + " module(s) {0}".format(self.done))
            return
        else:
            self.resultBox.setText("Completed search with all modules!")
            self.log.info("Completed search with all modules!")
            for mod in self.done:
                self.populateSearchList(mod)
            self.done.clear()

    def search(self) -> None:
        """SEARCH PHASE 1 Called after clicking on the search button"""
        modules = []
        # Dynamic import of modules (inside 'modules' folder)
        for f in os.listdir(os.path.normpath(os.getcwd() + "/Modules")):
            if (".py" in f):
                print(f)
                # Only add module to the modules array if module's setting 'Enable module' is true
                f = f.replace(".py", "")
                imported = importlib.import_module("." + f, "Modules")
                for s in self.modulesSettings:
                    if s.name == f:
                        if s.enableThis.isChecked():
                            modules.append(imported.module())
        self.listSearchWorkers = []
        self.listGamesWorkers = []
        self.listIconsWorkers = []
        self.done = []
        self.infos = []
        self.pending = len(modules)
        self.downloadCounter = -1
        self.linksListWidget.clear()
        # Repeat this for each module
        for module in modules:
            # Clear any previous garbage
            self.listWidget.clear()
            self.linksListWidget.clear()

            # Create and start n searchGamesWorker threads and put them in a n-list
            self.log.info("PHASE 1 SEARCHING {0} with {1}".format(self.searchBox.text(), module.name))
            self.listSearchWorkers.append(searchGamesWorker(module, self.searchBox.text()))
            self.listSearchWorkers[len(self.listSearchWorkers) - 1].start()
            self.listSearchWorkers[len(self.listSearchWorkers) - 1].done.connect(self.lock)
            self.searchButton.setEnabled(False)

        self.log.info("Search phase ended")

        # Loading gif and modules progression
        self.movieLoading = QMovie(os.path.normpath(os.getcwd() + "/Icons/Loading.gif"))
        self.movieLoading.setScaledSize(QSize(self.properties.generalData["UIIconSizePx"] * 2, self.properties.generalData["UIIconSizePx"] * 2))
        self.movieBox.setMovie(self.movieLoading)
        self.resultBox.setText("Completed search with 0/" + str(self.pending) + " module(s)")
        self.movieLoading.start()

    def populateSearchList(self, module) -> None:
        """SEARCH PHASE 2 starts the worker tasked to fill the lefthand side of the GUI"""
        # We reach here with the threaded modules, we need to do the same thing as above
        self.log.info("Executing PHASE 2 with: {0} module".format(module[0].name))

        # This will be populated by search results with icons and game title
        self.listWidget.clear()
        self.linksListWidget.clear()
        self.resumeIcon.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/GameIcons/default.png")).scaled(self.properties.generalData["GameIconSizePx"] * 2,self.properties.generalData["GameIconSizePx"] * 2, Qt.KeepAspectRatio))
        self.resumeLabel.clear()

        # Create and start n-listGamesWorker thread and put them in a n-list
        self.listGamesWorkers.append(listGamesWorker(module[0]))
        self.listGamesWorkers[len(self.listGamesWorkers) - 1].start()
        self.listGamesWorkers[len(self.listGamesWorkers) - 1].done.connect(self.makeInfos)
        self.searchButton.setEnabled(True)

    def makeInfos(self, value):
        """SEARCH PHASE 3 Receives the return value of the search fuction of the module containing a 2-dimensional array value[0] = titles value[1] = links. If needed it also starts the worker tasked to fetch the games respective icons"""
        self.log.info("Executing PHASE 3 with: {0} module".format(value[1].name))
        # Retain a list of 2d arrays containing [0]titles [1]links
        self.infos.append(value[0])
        if self.properties.generalData["loadicons"] == 1:
            # Create and start listIconsWorker thread if loadIcons setting is True
            self.listIconsWorkers.append(iconGamesWorker(value[1]))
            self.listIconsWorkers[len(self.listIconsWorkers) - 1].start()
            self.listIconsWorkers[len(self.listIconsWorkers) - 1].done.connect(self.createList)
        else:
            # Pass to createList only the module's name
            self.createList([None, value[1]])

    def lock2(self, module):
        """Wait for all module's PHASE 3 to have finished"""
        self.done.append(module)
        if len(self.done) < self.pending:
            self.resultBox.setText("Finalized search with " + str(len(self.done)) + "/" + str(self.pending) + "module(s)")
            return False
        else:
            self.resultBox.setText("Finalized search with all mudles!")
            return True

    def createList(self, value):
        """SEARCH PHASE 4 Lists all the titles (+ icons) on the left and resets the state of the GUI"""
        self.str_titles = []
        self.str_links = []
        # Add condition to disable this function
        if self.properties.generalData["loadicons"] == 1:
            self.log.info("Executing PHASE 4 with: {0} module".format(value[1].name))
            self.icons = value[0][0]
            self.sizes = value[0][1]
            self.DownloadIcon(value[1], value[1].name)
        else:
            self.log.info("Executing PHASE 4 with: {0} module".format(value[1].name))
        # Get lock status
        if self.lock2(value[1]):
            try:
                counter = -1
                offset = -1
                for Set in self.infos:
                    offset = offset + 1
                    for k,v in enumerate(Set[0]):
                        counter = counter + 1
                        if self.properties.generalData["loadicons"] == 1:
                            self.listWidget.addItem(QListWidgetItem(QIcon(os.path.normpath(os.getcwd() + "/GameIcons/_" + self.done[offset].name + "_" + str(counter) + ".png")), str(v)))
                        else:
                            self.listWidget.addItem(QListWidgetItem(QIcon(os.path.normpath(os.getcwd() + "/GameIcons/default.png")), str(v)))
                        self.str_titles.append(v)
                        self.str_links.append((Set[1][k], offset))
                self.log.info("Waiting for USER to choose GAME")
            except TypeError as e:
                # No results found error
                self.log.error("NO RESULTS FOUND!")
                self.alarm("Error", "No results found!")
            self.listWidget.setIconSize(QSize((self.properties.generalData["GameIconSizePx"]), (self.properties.generalData["GameIconSizePx"])))
            self.resultBox.setText(self.greetings())
            self.movieBox.clear()# ENDREGION
# REGION Selection Phase
    def selectGame(self):
        """SELECTION PHASE 1 Once clicked on the desired game pass it to listLinksWorker"""
        self.linksListWidget.clear()

        # Make resume
        if self.properties.generalData["loadicons"] == 1:
            # Throws and out of bounds error when re-searching after selecting a game (no effects notable)
            self.resumeIcon.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/GameIcons/_" + self.done[self.str_links[self.listWidget.currentRow()][1]].name +  "_" + str(self.listWidget.currentRow()) + ".png")).scaled(self.properties.generalData["GameIconSizePx"] * 2,self.properties.generalData["GameIconSizePx"] * 2, Qt.KeepAspectRatio))
        else:
            self.resumeIcon.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/GameIcons/default.png")).scaled(self.properties.generalData["GameIconSizePx"] * 2,self.properties.generalData["GameIconSizePx"] * 2, Qt.KeepAspectRatio))            
        self.resumeLabel.setText(self.str_titles[self.listWidget.currentRow()])
        self.resumeLabel.setFont(QFont("Arial", self.properties.generalData["resumefont"]))
        self.resumeLayout.addWidget(self.resumeIcon)
        self.resumeLayout.addWidget(self.resumeLabel)
        self.log.info("USER selected {0}".format(self.str_titles[self.listWidget.currentRow()]))

        # Save the tuple element returned from listLinks
        # Create and start listLinksWorker thread
        if self.properties.generalData["loadicons"] == 1:
            self.linksWorker = listLinksWorker(self.done[self.str_links[self.listWidget.currentRow()][1]], self.str_links[self.listWidget.currentRow()][0])
        else:
            self.linksWorker = listLinksWorker(self.done[self.str_links[self.listWidget.currentRow()][1]], self.str_links[self.listWidget.currentRow()][0])
        self.linksWorker.start()
        self.linksWorker.done.connect(self.displayLinks)

        self.movieLoading = QMovie(os.path.normpath(os.getcwd() + "/Icons/Loading.gif"))
        self.movieLoading.setScaledSize(QSize(self.properties.generalData["UIIconSizePx"] * 2, self.properties.generalData["UIIconSizePx"] * 2))
        self.movieBox.setMovie(self.movieLoading)
        self.movieLoading.start()

    def displayLinks(self, tupleElement: "tuple[list, list]") -> None:
        """SELECTION PHASE 2 Lists the games link(s) on the right-side box"""
        self.linksListWidget.clear()
        for k,v in enumerate(tupleElement[0]):
            # Entries
            if tupleElement[1][k] != "- ":
                item = QListWidgetItem(tupleElement[1][k] + " " + v)
                if self.properties.generalData["theme"] == "Dark":
                    item.setForeground(QColor("green"))
                if self.properties.generalData["theme"] == "Aqua":
                    item.setForeground(QColor("green"))
                if self.properties.generalData["theme"] == "Light":
                    item.setForeground(QColor("blue"))
                if self.properties.generalData["theme"] == "Patriotic":
                    item.setForeground(QColor("white"))
            # Links
            else:
                item = QListWidgetItem("- " + v)
                if self.properties.generalData["theme"] == "Dark":
                    item.setForeground(QColor("white"))
                if self.properties.generalData["theme"] == "Aqua":
                    item.setForeground(QColor("white"))
                if self.properties.generalData["theme"] == "Light":
                    item.setForeground(QColor("black"))
                if self.properties.generalData["theme"] == "Patriotic":
                    item.setForeground(QColor("green"))
            # Printing links on the rightside box
            self.linksListWidget.addItem(item)
        self.resultBox.setText(self.greetings())
        self.movieBox.clear()# ENDREGION
# REGION Link Fetching
    def fetchDownloadLink(self) -> None:
        """LINK_FETCHING PHASE 1 Passes the selected entry+link to the module's cleaning function"""
        self.movieLoading = QMovie(os.path.normpath(os.getcwd() + "/Icons/Loading.gif"))
        self.movieLoading.setScaledSize(QSize(self.properties.generalData["UIIconSizePx"] * 2, self.properties.generalData["UIIconSizePx"] * 2))
        self.movieBox.setMovie(self.movieLoading)
        self.movieLoading.start()
        try:
            # Create and start cleanLinkWorker thread
            self.log.info("Cleaning {0}".format(self.linksListWidget.selectedItems()[0].text()))
            self.cleanWorker = cleanLinkWorker(self.done[self.str_links[self.listWidget.currentRow()][1]], self.linksListWidget.selectedItems()[0].text())
            self.cleanWorker.start()
            self.cleanWorker.done.connect(self.outputLink)
            # Disable links list
            self.linksListWidget.setDisabled(True)
        except:
            pass

    def outputLink(self, link: str):
        """LINK_FETCHING PHASE 2 link(str) contains the cleaned link"""
        # Re-enable links list
        self.linksListWidget.setDisabled(False)
        self.log.info("Cleaned link: {0}".format(link))
        if "http" or "magnet" in link:
            # If openLinks in config.json is set to 1/True, open the link in the browser
            if self.properties.generalData["openLinks"] == 1:
                self.directBrowser(link)
            # Ask the user to copy/open the link
            elif self.properties.generalData["openLinks"] == 0:
                self.linkPopUp("Success!", link)
        else:
            self.log.warning("Clicked on {0}".format(link))
            self.resultBox.setText("Error: The entry you choose is not a link!")
            self.movieBox.clear()# ENDREGION
# REGION Gui
    def setWindowParameters(self) -> None:
        # Title of main widget
        self.widget.setWindowTitle("SwitchGamesDownloader")

        # Icon of main widget
        self.widget.setWindowIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/Switch.png")))

        # Default size of GUI
        self.widget.resize(int(self.properties.generalData["Width"]), int(self.properties.generalData["Height"]))

        # Theme
        self.widget.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())

    def createLayout(self) -> None:
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

    def closeWindow(self) -> None:
        exit()

    def preferencesWindow(self) -> None:
        self.properties.widget.exec_()
        # Reload properties
        self.properties = self.properties.update()
        self.updatePreferences()

    def aboutWindow(self) -> None:
        self.a = About()

    def updatePreferences(self) -> None:
        """Real-time properties application"""
        self.listWidget.setIconSize(QSize((int(self.properties.generalData["GameIconSizePx"])), (int(self.properties.generalData["GameIconSizePx"]))))
        self.searchButton.setIconSize(QSize((int(self.properties.generalData["UIIconSizePx"])), (int(self.properties.generalData["UIIconSizePx"]))))
        self.widget.resize(int(self.properties.generalData["Width"]), int(self.properties.generalData["Height"]))
        self.widget.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.properties.generalData["theme"] + ".css"), "r").read())
    
    def createWidgets(self) -> None:
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
        self.searchButton.setIcon(QIcon(os.path.normpath(os.getcwd() + "/Icons/WebScraping.png")))
        self.searchButton.setIconSize(QSize((int(self.properties.generalData["UIIconSizePx"])), (int(self.properties.generalData["UIIconSizePx"]))))
        self.searchButton.setShortcut("Return")
        self.searchFunctionLayout.addWidget(self.searchButton)

        # Resume widget
        self.resumeIcon = QLabel()
        self.resumeLabel = QLabel()
        self.resumeIcon.setPixmap(QPixmap(os.path.normpath(os.getcwd() + "/GameIcons/default.png")).scaled(int(self.properties.generalData["GameIconSizePx"]) * 2,int(self.properties.generalData["GameIconSizePx"]) * 2, Qt.KeepAspectRatio))
        self.resumeLayout.addWidget(self.resumeIcon)
        self.resumeLayout.addWidget(self.resumeLabel)

        # Final Output Box
        self.resultBox = QLabel()
        self.movieBox = QLabel()

        # Add random greetings
        self.resultBox.setText(self.greetings())
        self.movieBox.setText("")

        # Bottom-right list with all download links
        self.linksListWidget = QListWidget()
        self.searchLayout.addWidget(self.linksListWidget)
        self.searchLayout.addWidget(self.movieBox)
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
        self.about.triggered.connect(self.aboutWindow)# ENDREGION

if __name__ == "__main__":
    App(True)
