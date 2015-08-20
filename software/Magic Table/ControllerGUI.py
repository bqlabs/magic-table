from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os

__author__ = 'def'


class ControllerGUI(QtGui.QWidget):

    defaultBaudrate = '115200'

    def __init__(self, parent, machine):
        QtGui.QWidget.__init__(self, parent)

        self.machine = machine
        self.currentPort = None
        self.currentBaudrate = self.defaultBaudrate
        self.form = None

        self.loadUI()

    def loadUI(self):
        # Load UI
        load_ui(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'ControllerGUI.ui'), self)
        self.form = self.findChild(QtGui.QWidget)

        # Connect things to UI slots to enable functionality
        self.set_available_ports()
        self.set_available_baudrates()
        self.form.portRefreshButton.clicked.connect(self.onPortButton)
        self.form.connectButton.clicked.connect(self.onConnectButton)
        self.form.resetButton.clicked.connect(self.onResetButton)

        self.form.speedLineEdit.setEnabled(False)
        self.form.homeButton.clicked.connect(self.onHomeButton)
        self.form.homeButton.setEnabled(False)
        self.setMoveControlsEnabled(False)
        self.form.upButton.clicked.connect(self.onMoveUpButton)
        self.form.downButton.clicked.connect(self.onMoveDownButton)
        self.form.leftButton.clicked.connect(self.onMoveLeftButton)
        self.form.rightButton.clicked.connect(self.onMoveRightButton)
        self.form.keyboardCheckBox.stateChanged.connect(self.setFocus)

    def set_available_ports(self):
        self.form.portComboBox.clear()
        ports = CoreXY.get_available_ports()
        self.form.portComboBox.addItems(ports)

    def set_available_baudrates(self):
        self.form.baudrateComboBox.clear()
        self.form.baudrateComboBox.addItems(CoreXY.get_available_baudrates())
        self.form.baudrateComboBox.setCurrentIndex(self.form.baudrateComboBox.findText(self.defaultBaudrate))

    def onPortButton(self):
        self.set_available_ports()

    def onConnectButton(self):
        # Disable buttons when disconnected
        if self.form.connectButton.text() == 'Connect':
            try:
                self.machine.port=self.form.portComboBox.currentText()
                self.machine.baudrate=self.form.baudrateComboBox.currentText()
                self.machine.connect()

                self.form.connectButton.setText('Disconnect')
                self.form.statusLabel.setText('Status: connected')
                self.form.homeButton.setEnabled(True)
            except:
                self.form.statusLabel.setText('Status: Error')
        elif self.form.connectButton.text() == 'Disconnect':
            try:
                self.machine.disconnect()

                self.form.connectButton.setText('Connect')
                self.form.statusLabel.setText('Status: disconnected')
                self.form.homeButton.setEnabled(False)
                self.setMoveControlsEnabled(False)
            except:
                self.form.statusLabel.setText('Status: Error')

    def onResetButton(self):
        self.machine.reset()
        self.form.statusLabel.setText('Status: Reset')

    def onHomeButton(self):
        self.machine.home()
        self.setMoveControlsEnabled(True)

    def setMoveControlsEnabled(self, state):
        self.form.leftButton.setEnabled(state)
        self.form.rightButton.setEnabled(state)
        self.form.upButton.setEnabled(state)
        self.form.downButton.setEnabled(state)
        self.form.precisionCheckBox.setEnabled(state)
        self.form.keyboardCheckBox.setEnabled(state)

    def onMoveUpButton(self):
        if self.form.precisionCheckBox.isChecked():
            self.machine.move_inc(0,1)
        else:
            self.machine.move_inc(0,10)

    def onMoveDownButton(self):
        if self.form.precisionCheckBox.isChecked():
            self.machine.move_inc(0,-1)
        else:
            self.machine.move_inc(0,-10)

    def onMoveLeftButton(self):
        if self.form.precisionCheckBox.isChecked():
            self.machine.move_inc(-1,0)
        else:
            self.machine.move_inc(-10,0)

    def onMoveRightButton(self):
        if self.form.precisionCheckBox.isChecked():
            self.machine.move_inc(1,0)
        else:
            self.machine.move_inc(10,0)

    def keyPressEvent(self, e):
        if self.findChild(QtGui.QWidget).keyboardCheckBox.isChecked():
            if e.key() ==QtCore.Qt.Key_Up:
                self.onMoveUpButton()
            elif e.key() ==QtCore.Qt.Key_Down:
                self.onMoveDownButton()
            elif e.key() ==QtCore.Qt.Key_Left:
                self.onMoveLeftButton()
            elif e.key() ==QtCore.Qt.Key_Right:
                self.onMoveRightButton()
            else:
                e.ignore()
        else:
            e.ignore()

    def closeEvent(self, event):
        if self.machine:
            self.machine.disconnect()
        event.accept()

    def focusOutEvent(self, event):
        self.setFocus()


class ToolheadWidgetFactory:
    def __init__(self):
        pass

    def loadUI(self):
        pass

    def createWidget(self, type):
        pass


if __name__ == '__main__':
    from CoreXY import CoreXY
    from SimpleMagnetToolhead import SimpleMagnetToolhead

    app = QtGui.QApplication(sys.argv)

    cxy = CoreXY()
    tool = SimpleMagnetToolhead(4,5)
    cxy.set_toolhead(tool)

    gui = ControllerGUI(None, cxy)
    gui.show()
    # gui.form.show()

    sys.exit(app.exec_())