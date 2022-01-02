from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import json
import os

class Preferences():
    def __init__(self, moduleList: list) -> None:
        self.moduleList = moduleList
        # Load gui configs
        with open("config.json",) as f:
            try:
                self.generalData = json.load(f)["General"]
            except KeyError:
                # Load default config
                self.generalData = {
                    "Width": 1920,
                    "Height": 1080,
                    "GameIconSizePx": 100,
                    "UIIconSizePx": 20,
                    "theme": "light",
                    "resumefont": 15,
                    "loadicons": 1,
                    "openLinks": 0
                }
        # Load version.json file
        with open("version.json",) as f:
            self.version = json.load(f)
            f.close()

        self.mainLayout = QVBoxLayout()

        # Main widget
        self.widget = QDialog()
        self.widget.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.generalData["theme"] + ".css"), "r").read())

        # Set window title
        self.widget.setWindowTitle("Preferences")

        # Neat Labels
        self.label = QLabel("Preferences Menu")

        # Instantiate QTabWidget to store all tabs of modules configuration
        self.folder = QTabWidget()

        # Icon of widget
        self.widget.setWindowIcon(QIcon("Icons\\Switch.png"))

        # General close button
        self.ok = QPushButton("Close")
        self.ok.clicked.connect(self.saveClose)

        # Take priority over mainWindow
        self.widget.setWindowModality(Qt.ApplicationModal)
        for module in moduleList:
            self.folder.addTab(module.widget, module.name)
        
# REGION general tab
        # Create preferences tab
        self.general = QWidget()

        # Layouts
        self.form = QFormLayout()
        self.general.setLayout(self.form)

        # TickBoxes
        self.loadIcons = QCheckBox()
        self.openLinks = QCheckBox()

        # TextBoxes
        self.widthTextBox = QLineEdit("800")
        self.heightTextBox = QLineEdit("600")
        self.GameIconSizePxTextBox = QLineEdit("100")
        self.UIIconSizePxTextBox = QLineEdit("30")
        self.ResumefontsizeTextBox = QLineEdit("25")

        # DropdownBox
        self.themes = QComboBox()
        self.themes.addItems(["Light", "Dark", "Aqua", "Patriotic"])

        # Assign to form layout
        self.form.addRow("Theme", self.themes)
        self.form.addRow("Width", self.widthTextBox)
        self.form.addRow("Height", self.heightTextBox)
        self.form.addRow("Game Icon Size Px", self.GameIconSizePxTextBox)
        self.form.addRow("UI Icon Size Px", self.UIIconSizePxTextBox)
        self.form.addRow("Resume font size", self.ResumefontsizeTextBox)
        self.form.addRow("Load icons", self.loadIcons)
        self.form.addRow("Always open link",self.openLinks)

        # Self-assign config
        self.widthTextBox.setText(str(self.generalData["Width"]))
        self.heightTextBox.setText(str(self.generalData["Height"]))
        self.GameIconSizePxTextBox.setText(str(self.generalData["GameIconSizePx"]))
        self.UIIconSizePxTextBox.setText(str(self.generalData["UIIconSizePx"]))
        self.themes.setCurrentText(self.generalData["theme"])
        self.ResumefontsizeTextBox.setText(str(self.generalData["resumefont"]))
        self.loadIcons.setChecked(bool(self.generalData["loadicons"]))
        self.openLinks.setChecked(bool(self.generalData["openLinks"]))

        #Listeners
        self.widthTextBox.textChanged.connect(self.stateChange)
        self.heightTextBox.textChanged.connect(self.stateChange)
        self.GameIconSizePxTextBox.textChanged.connect(self.stateChange)
        self.UIIconSizePxTextBox.textChanged.connect(self.stateChange)
        self.themes.currentIndexChanged.connect(self.stateChange)
        self.ResumefontsizeTextBox.textChanged.connect(self.stateChange)
        self.loadIcons.stateChanged.connect(self.stateChange)
        self.openLinks.stateChanged.connect(self.stateChange)

# ENDREGION
        # Add general tab
        self.folder.addTab(self.general, "General")
        self.mainLayout.addWidget(self.folder)
        self.mainLayout.addWidget(self.ok)
        self.widget.setLayout(self.mainLayout)

    def update(self):
        return self

    def saveClose(self) -> None:
        """Gather all self.data from the modules and dumps it into config.json"""
        # Serialize generalData into a dict
        value = { "General" : {} }
        for entry in self.generalData:
            value["General"][entry] = self.generalData[entry]
        
        with open("config.json", "w") as f:
            for module in self.moduleList:
                self.serialize(module, value)
            json.dump(value, f)
            # Update self.generalData to avoid reinitializing the class
            self.generalData = value["General"]
            self.widget.setStyleSheet(open(os.path.normpath(os.getcwd() + "/Themes/" + self.generalData["theme"] + ".css"), "r").read())
        
        self.widget.close()

    def serialize(self, module, v: "dict[str, dict]") -> None:
        """Serialize m.data into a dict"""
        v[module.name] = {}
        for entry in module.data:
            v[module.name][entry] = module.data[entry]

    def stateChange(self) -> None:
        if self.loadIcons.isChecked(): self.generalData["loadicons"] = 1
        else: self.generalData["loadicons"] = 0

        if self.openLinks.isChecked(): self.generalData["openLinks"] = 1
        else: self.generalData["openLinks"] = 0

        # Width/Height failsafe
        try:
            self.generalData["Width"] = int(self.widthTextBox.text())
            self.generalData["Height"] = int(self.heightTextBox.text())
        except ValueError:
            pass

        # GameIconSizePx/UIIconSizePx failsafe
        try:
            self.generalData["GameIconSizePx"] = int(self.GameIconSizePxTextBox.text())
            self.generalData["UIIconSizePx"] = int(self.UIIconSizePxTextBox.text())
        except ValueError:
            pass
        # ResumeFontSize failsafe
        try:
            self.generalData["resumefont"] = int(self.ResumefontsizeTextBox.text())
        except ValueError:
            pass
        
        # Theme changer
        self.generalData["theme"] = self.themes.currentText()

    def bool(self, line) -> bool:
        """Returns 1 or 0 depending on True/False from config.json"""
        if "True" or 1 in line:
            return True
        if "False" or 0 in line:
            return False
