# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QWidget, QPlainTextEdit, QPushButton, QTextBrowser, QCheckBox
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtXml
import PySide2
import screen

class gui(QWidget):
    def __init__(self):
        super(gui, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)

        loader.load(ui_file, self)

        self.button = self.findChild(QPushButton, 'pushButton')
        self.button.clicked.connect(self.buttonPressed)
        self.starts = self.findChild(QPushButton, 'pushButton_2')
        self.starts.clicked.connect(self.start)
        ui_file.close()

    def start(self):
        stash = {"left": 17, "top": 150, "width": 580, "height": 580}
        screen.make_screenshot(stash)
        res = screen.find_bright('screenshot.png')
        self.price = self.findChild(QTextBrowser, 'result')
        self.price.append(str(res))

    def buttonPressed(self):
        from get_price import get_price
        input = self.findChild(QPlainTextEdit, 'name')

        self.price = self.findChild(QTextBrowser, 'result')
        headless = self.findChild(QCheckBox, 'headless').isChecked()
        print(headless)
        input=input.toPlainText()
        print(input)

        pric = get_price(str.join("\n", input.splitlines()), headless)
        self.price.setText(pric)


if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())
