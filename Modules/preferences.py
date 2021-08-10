from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Modules.Workers.adBlockerDownloaderWorker import adBlockerDownloaderWorker
import json
import os

class Preferences():
    def __init__(self):
        # Load config.json file
        with open("config.json",) as f:
            self.data = json.load(f)
            f.close()
        
        # Load version.json file
        with open("version.json",) as f:
            self.version = json.load(f)
            f.close()

        # Main widget
        self.widget = QDialog()
        self.widget.setStyleSheet(open("Themes\\" + self.data["theme"] + ".css", "r").read())

        # Icon of widget
        self.widget.setWindowIcon(QIcon("Icons\\Switch.png"))
        
        # Take priority over mainWindow
        self.widget.setWindowModality(Qt.ApplicationModal)

        # Layouts
        self.mainLayout = QVBoxLayout()
        self.topCenter = QVBoxLayout()
        self.tickBoxes = QGridLayout()
        self.buttonLayout = QVBoxLayout()
        self.form = QFormLayout()

        # Build mainLayout
        self.mainLayout.addLayout(self.topCenter)
        self.mainLayout.addLayout(self.tickBoxes)
        self.mainLayout.addLayout(self.form)
        self.mainLayout.addLayout(self.buttonLayout)

        #Set window title
        self.widget.setWindowTitle("Preferences")

        # Neat Labels
        self.label = QLabel("Preferences Menu")

        # Set mainLayout
        self.widget.setLayout(self.mainLayout)

        # TickBoxes
        self.loadIcons = QCheckBox("Load Icons")
        self.openLinks = QCheckBox("Always open links in the browser")
        self.semiAuto = QCheckBox("Semi-auto mode")
        self.adBlocker = QCheckBox("AdBlocker")

        # TextBoxes
        self.widthTextBox = QLineEdit("800")
        self.heightTextBox = QLineEdit("600")
        self.GameIconSizePxTextBox = QLineEdit("100")
        self.UIIconSizePxTextBox = QLineEdit("30")
        self.ResumefontsizeTextBox = QLineEdit("25")

        # DropdownBox
        self.themes = QComboBox()
        self.themes.addItems(["Light", "Dark", "Aqua", "Patriotic"])

        # Buttons
        self.ok = QPushButton("Close")
        

        # Assign to layout
        self.topCenter.addWidget(self.label)
        self.tickBoxes.addWidget(self.loadIcons, 0, 0)
        self.tickBoxes.addWidget(self.openLinks, 1, 0)
        self.tickBoxes.addWidget(self.semiAuto, 2, 0)
        self.tickBoxes.addWidget(self.adBlocker, 3, 0)
        self.buttonLayout.addWidget(self.ok)

        # Assign to form layout
        self.form.addRow("Theme", self.themes)
        self.form.addRow("Width", self.widthTextBox)
        self.form.addRow("Height", self.heightTextBox)
        self.form.addRow("Game Icon Size Px", self.GameIconSizePxTextBox)
        self.form.addRow("UI Icon Size Px", self.UIIconSizePxTextBox)
        self.form.addRow("Resume font size", self.ResumefontsizeTextBox)

        # Self-apply config.json
        self.loadIcons.setChecked(bool(self.data["loadicons"]))
        self.openLinks.setChecked(bool(self.data["openLinks"]))
        self.semiAuto.setChecked(bool(self.data["semiAutoMode"]))
        self.adBlocker.setChecked(bool(self.data["adBlock"]))
        self.widthTextBox.setText(str(self.data["Width"]))
        self.heightTextBox.setText(str(self.data["Height"]))
        self.GameIconSizePxTextBox.setText(str(self.data["GameIconSizePx"]))
        self.UIIconSizePxTextBox.setText(str(self.data["UIIconSizePx"]))
        self.themes.setCurrentText(self.data["theme"])
        self.ResumefontsizeTextBox.setText(str(self.data["resumefont"]))

        # Set tooltips 
        self.semiAuto.setToolTip("ON: The user will be asked to solve the Captcha, once solved the script will continue on it's own<br>OFF: The program will only reach the Captcha page, you will need to continue on your own")
        self.adBlocker.setToolTip("ON: Disables intrusive ads ONLY in Captcha page<br>OFF: Renders ALL the ads in the Captcha page<br>Personal Note: Leave this unchecked as ads supports the website's owner(s)")

        # Define listeners
        self.loadIcons.stateChanged.connect(self.stateChange)
        self.openLinks.stateChanged.connect(self.stateChange)
        self.semiAuto.stateChanged.connect(self.stateChange)
        self.adBlocker.stateChanged.connect(self.stateChange)
        self.widthTextBox.textChanged.connect(self.stateChange)
        self.heightTextBox.textChanged.connect(self.stateChange)
        self.GameIconSizePxTextBox.textChanged.connect(self.stateChange)
        self.UIIconSizePxTextBox.textChanged.connect(self.stateChange)
        self.themes.currentIndexChanged.connect(self.stateChange)
        self.ResumefontsizeTextBox.textChanged.connect(self.stateChange)
        self.ok.clicked.connect(self.saveClose)

    def closeDownloadingAdBlocker(self, value):
        self.pbar.setValue(value)
        if (value >= 99):
            self.closeButton.setEnabled(True)
            self.downloadAdBlockerMessage.close()

    def stateChange(self):
        if self.loadIcons.isChecked(): self.data["loadicons"] = 1
        else: self.data["loadicons"] = 0

        if self.openLinks.isChecked(): self.data["openLinks"] = 1
        else: self.data["openLinks"] = 0

        if self.semiAuto.isChecked(): self.data["semiAutoMode"] = 1
        else: self.data["semiAutoMode"] = 0

        if self.adBlocker.isChecked():
            self.data["adBlock"] = 1
            if (os.path.isfile(os.getcwd() + "\\Modules\\adblock.crx")):
                pass
            else:
                # Define message box + layout
                self.downloadAdBlockerMessage = QMessageBox()
                self.downloadAdBlockerMessageLayout = self.downloadAdBlockerMessage.layout()
                
                # Define messageBox default button
                self.closeButton = QPushButton(" Close")
                self.downloadAdBlockerMessage.addButton(self.closeButton, QMessageBox.YesRole)

                # Define and set ProgressBar
                self.pbar = QProgressBar()
                self.downloadAdBlockerMessageLayout.addWidget(self.pbar, 1, 0)

                # Set window stuff
                self.downloadAdBlockerMessage.setWindowTitle("Downloading...")
                self.adBlockLabel = QLabel("Getting the AdBlocker for you <3!")
                self.downloadAdBlockerMessageLayout.addWidget(self.adBlockLabel, 0, 0)
                self.downloadAdBlockerMessage.setStyleSheet(open("Themes\\" + self.data["theme"] + ".css", "r").read())

                # Start adBlocker downloader worker
                self.adBlockerDownloader = adBlockerDownloaderWorker()
                self.adBlockerDownloader.start()
                self.adBlockerDownloader.updated.connect(self.closeDownloadingAdBlocker)
                self.closeButton.setEnabled(False)

                # Execute
                self.downloadAdBlockerMessage.exec_()
        else:
            self.data["adBlock"] = 0
        
        # Width/Height failsafe
        try:
            self.data["Width"] = int(self.widthTextBox.text())
            self.data["Height"] = int(self.heightTextBox.text())
        except ValueError:
            pass

        # GameIconSizePx/UIIconSizePx failsafe
        try:
            self.data["GameIconSizePx"] = int(self.GameIconSizePxTextBox.text())
            self.data["UIIconSizePx"] = int(self.UIIconSizePxTextBox.text())
        except ValueError:
            pass
        # ResumeFontSize failsafe
        try:
            self.data["resumefont"] = int(self.ResumefontsizeTextBox.text())
        except ValueError:
            pass
        
        # Theme changer
        self.data["theme"] = self.themes.currentText()

        # Save config.json
        with open("config.json", "w") as f:
            json.dump(self.data, f)

    def saveClose(self):
        self.stateChange()
        self.widget.close()

    def bool(self, line):
        """Returns 1 or 0 depending on True/False from config.json"""
        if "True" or 1 in line:
            return True
        if "False" or 0 in line:
            return False
