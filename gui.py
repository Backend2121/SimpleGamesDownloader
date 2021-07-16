import os
from about import About
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from preferences import Preferences
from SGD import SGD
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

    def openGithub(self):
        """Open latest release on GitHub"""
        webbrowser.open("https://github.com/Backend2121/SwitchGamesDownloader/releases/latest")

    def checkUpdates(self):
        version = os.popen("curl https://github.com/Backend2121/SwitchGamesDownloader/releases/latest").read()
        urlStart = version.find("/tag/")
        urlEnd = version.find('">')
        if version[urlStart+5:urlEnd] == self.properties.data["version"]:
            pass
        else:
            self.updateAvailable("Update found", "A new version of this software is available on GitHub!")

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

    def greetings(self):
        greets = ["Hi!", "Hello there!", "Hey!", "Honk!", "Whassup!", "I promise i won't hang", "What do you need?", "Here to help!", "How are you doing?", "Join the Discord!"]
        return greets[random.randrange(0,len(greets))]

    def DownloadIcon(self):
        for k,icon in enumerate(self.icons):
            # Download image
            self.sgd.browser.get(icon)
            self.sgd.browser.save_screenshot("GameIcons\\" + str(k) + ".png")
            # Resize image
            self.sgd.cropImage("GameIcons\\" + str(k) + ".png", self.sizes[k])

    def search(self):
        self.listWidget.clear()
        self.linksListWidget.clear()
        try:
            if self.sgd in locals(): pass
        except:
            self.sgd = SGD()
        self.searchText = self.searchBox.text()
        self.sgd.searchGame(self.searchText)
        # Attach to first part of SGD.py
        self.populateSearchList()

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
        tupleElement = self.sgd.listLinks(self.infos[1][0][self.listWidget.currentRow()])
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

    def fetchDownloadLink(self):
        try:
            link = self.sgd.CleanLink(self.linksListWidget.selectedItems()[0].text())
            # Ads skipping and stuff inside SGD.py
            if link != None:
                self.linkPopUp("Success!", link)
            else:
                self.resultBox.setText("Error: The entry you choose is not a link!")
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
    
    def populateSearchList(self):
        # This will be populated by search results with icons and game title
        self.listWidget.clear()
        self.linksListWidget.clear()
        self.resumeIcon.setPixmap(QPixmap("GameIcons\\default.png").scaled(self.properties.data["GameIconSizePx"] * 2,self.properties.data["GameIconSizePx"] * 2, Qt.KeepAspectRatio))
        self.resumeLabel.clear()
        self.infos = self.sgd.listGames()
        if self.infos == 1:
            self.search()
        if self.properties.data["loadicons"] == 1:
            self.icons = self.sgd.listIcons()[0]
            self.sizes = self.sgd.listIcons()[1]
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
