from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os
from CoreXY import CoreXY

__author__ = 'def'


class ControllerGUI(QtGui.QWidget):

    defaultBaudrate = '115200'

    def __init__(self, parent, machine):
        QtGui.QWidget.__init__(self, parent)

        self.machine = machine
        self.currentPort = None
        self.currentBaudrate = self.defaultBaudrate

        # References to widgets
        self.portComboBox = None
        self.baudrateComboBox = None
        self.portRefreshButton = None
        self.connectButton = None
        self.resetButton = None
        self.speedLineEdit = None
        self.homeButton = None
        self.leftButton = None
        self.rightButton = None
        self.upButton = None
        self.downButton = None
        self.precisionCheckBox = None
        self.keyboardCheckBox = None
        self.toolsGroupBox = None
        self.statusLabel = None
        self.xPosLabel = None
        self.yPosLabel = None

        self.loadUI()
        self.add_tools()

    def loadUI(self):
        # Load UI
        main_widget = load_ui(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'ControllerGUI.ui'), self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)

        # Get references to widgets
        self.portComboBox = self.findChild(QtGui.QComboBox, "portComboBox")
        self.baudrateComboBox = self.findChild(QtGui.QComboBox, "baudrateComboBox")
        self.portRefreshButton = self.findChild(QtGui.QPushButton, "portRefreshButton")
        self.connectButton = self.findChild(QtGui.QPushButton, "connectButton")
        self.resetButton = self.findChild(QtGui.QPushButton, "resetButton")
        self.speedLineEdit = self.findChild(QtGui.QLineEdit, "speedLineEdit")
        self.homeButton = self.findChild(QtGui.QPushButton, "homeButton")
        self.leftButton = self.findChild(QtGui.QPushButton, "leftButton")
        self.rightButton = self.findChild(QtGui.QPushButton, "rightButton")
        self.upButton = self.findChild(QtGui.QPushButton, "upButton")
        self.downButton = self.findChild(QtGui.QPushButton, "downButton")
        self.precisionCheckBox = self.findChild(QtGui.QCheckBox, "precisionCheckBox")
        self.keyboardCheckBox = self.findChild(QtGui.QCheckBox, "keyboardCheckBox")
        self.toolsGroupBox = self.findChild(QtGui.QGroupBox, "toolsGroupBox")
        self.statusLabel = self.findChild(QtGui.QLabel, "statusLabel")
        self.xPosLabel = self.findChild(QtGui.QLabel, "xPosLabel")
        self.yPosLabel = self.findChild(QtGui.QLabel, "yPosLabel")



        # Connect things to UI slots to enable functionality
        self.set_available_ports()
        self.set_available_baudrates()
        self.portRefreshButton.clicked.connect(self.onPortButton)
        self.connectButton.clicked.connect(self.onConnectButton)
        self.resetButton.clicked.connect(self.onResetButton)

        self.speedLineEdit.setEnabled(False)
        self.homeButton.clicked.connect(self.onHomeButton)
        self.homeButton.setEnabled(False)
        self.setMoveControlsEnabled(False)
        self.upButton.clicked.connect(self.onMoveUpButton)
        self.downButton.clicked.connect(self.onMoveDownButton)
        self.leftButton.clicked.connect(self.onMoveLeftButton)
        self.rightButton.clicked.connect(self.onMoveRightButton)
        self.keyboardCheckBox.stateChanged.connect(self.setFocus)

        self.toolsGroupBox.setEnabled(False)

    def add_tools(self):
        if self.machine.toolhead.type == 'SimpleMagnet':
            from SimpleMagnetToolhead import SimpleMagnetToolheadWidget
            w = SimpleMagnetToolheadWidget(None, self.machine.toolhead)
            self.toolsGroupBox.setLayout(w)
        elif self.machine.toolhead.type == 'SimpleMagnetMockup':
            from SimpleMagnetToolheadMockup import SimpleMagnetToolheadMockupWidget
            w = SimpleMagnetToolheadMockupWidget(None, self.machine)
            self.toolsGroupBox.setLayout(w)
        else:
            raise AttributeError("Toolhead type not supported yet!")

    def set_available_ports(self):
        self.portComboBox.clear()
        ports = self.machine.get_available_ports()
        self.portComboBox.addItems(ports)

    def set_available_baudrates(self):
        self.baudrateComboBox.clear()
        self.baudrateComboBox.addItems(self.machine.get_available_baudrates())
        self.baudrateComboBox.setCurrentIndex(self.baudrateComboBox.findText(self.defaultBaudrate))

    def onPortButton(self):
        self.set_available_ports()

    def onConnectButton(self):
        # Disable buttons when disconnected
        if self.connectButton.text() == 'Connect':
            try:
                self.machine.port=self.portComboBox.currentText()
                self.machine.baudrate=self.baudrateComboBox.currentText()
                self.machine.connect()

                self.connectButton.setText('Disconnect')
                self.statusLabel.setText('Status: connected')
                self.homeButton.setEnabled(True)
                self.toolsGroupBox.setEnabled(True)
            except CoreXY.ConnectException:
                self.statusLabel.setText('Status: Error')
        elif self.connectButton.text() == 'Disconnect':
            try:
                self.machine.disconnect()

                self.connectButton.setText('Connect')
                self.statusLabel.setText('Status: disconnected')
                self.homeButton.setEnabled(False)
                self.setMoveControlsEnabled(False)
                self.toolsGroupBox.setEnabled(False)
            except CoreXY.ConnectException:
                self.statusLabel.setText('Status: Error')
            finally:
                self.updatePos()

    def onResetButton(self):
        self.machine.reset()
        self.statusLabel.setText('Status: Reset')
        self.updatePos()

    def onHomeButton(self):
        self.machine.home()
        self.setMoveControlsEnabled(True)
        self.updatePos()

    def setMoveControlsEnabled(self, state):
        self.leftButton.setEnabled(state)
        self.rightButton.setEnabled(state)
        self.upButton.setEnabled(state)
        self.downButton.setEnabled(state)
        self.precisionCheckBox.setEnabled(state)
        self.keyboardCheckBox.setEnabled(state)

    def onMoveUpButton(self):
        if self.precisionCheckBox.isChecked():
            self.machine.move_inc(0,1)
        else:
            self.machine.move_inc(0,10)
        self.updatePos()

    def onMoveDownButton(self):
        if self.precisionCheckBox.isChecked():
            self.machine.move_inc(0,-1)
        else:
            self.machine.move_inc(0,-10)
        self.updatePos()

    def onMoveLeftButton(self):
        if self.precisionCheckBox.isChecked():
            self.machine.move_inc(-1,0)
        else:
            self.machine.move_inc(-10,0)
        self.updatePos()

    def onMoveRightButton(self):
        if self.precisionCheckBox.isChecked():
            self.machine.move_inc(1,0)
        else:
            self.machine.move_inc(10,0)
        self.updatePos()

    def updatePos(self):
        if self.upButton.isEnabled():
            self.xPosLabel.setText('x: %d'%self.machine.x)
            self.yPosLabel.setText('y: %d'%self.machine.y)
        else:
            self.xPosLabel.setText('x: ?')
            self.yPosLabel.setText('y: ?')

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


if __name__ == '__main__':
    from SimpleMagnetToolhead import SimpleMagnetToolhead

    app = QtGui.QApplication(sys.argv)

    cxy = CoreXY()
    tool = SimpleMagnetToolhead(4,5)
    cxy.set_toolhead(tool)

    gui = ControllerGUI(None, cxy)
    gui.show()

    sys.exit(app.exec_())