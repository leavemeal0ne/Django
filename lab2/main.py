import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QHeaderView

from lab2.MainWindow import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
