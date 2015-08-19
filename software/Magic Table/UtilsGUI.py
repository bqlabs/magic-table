from PySide import QtCore
from PySide import QtUiTools
import os

__author__ = 'def'

def load_ui(file_name):
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(file_name)
    ui_file.open(QtCore.QFile.ReadOnly)
    myWidget = loader.load(ui_file, None)
    ui_file.close()
    return myWidget