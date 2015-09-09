from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os

from ControllerGUI import ControllerGUI
from CalibrationWidget import CalibrationWidget
from Calibration import Calibration
from TrajectoryWidget import TrajectoryWidget

__author__ = 'def'

class MagicTableMainWindow(QtGui.QWidget):
    def __init__(self, machine):
        # Init MainWindow
        super(MagicTableMainWindow, self).__init__()
        self.setWindowTitle('Magic Table')

        # Create main layout
        layout = QtGui.QHBoxLayout()

        # Load Control Panel
        self.machine = machine
        self.control_panel = ControllerGUI(None, machine)

        # Add widgets to main layout
        layout.addWidget(self.control_panel)
        self.setLayout(layout)

        # Add side toolbar
        self.buttonLayout = QtGui.QVBoxLayout()

        # Add calibration workspace button
        self.calibration = None
        self.calibrationWidget = None
        self.calibrationButton = QtGui.QPushButton('->')
        self.calibrationButton.setGeometry(0, 0, 64, 64)
        self.calibrationButton.setCheckable(True)
        self.calibrationButton.toggled.connect(self.onCalibrationButtonEnabled)
        self.buttonLayout.addWidget(self.calibrationButton)

        # Add path workspace button
        self.trajectoryWidget = None
        self.trajectoryButton = QtGui.QPushButton('path')
        self.trajectoryButton.setGeometry(0, 0, 64, 64)
        self.trajectoryButton.setCheckable(True)
        self.trajectoryButton.toggled.connect(self.onTrajectoryButtonEnabled)
        self.buttonLayout.addWidget(self.trajectoryButton)

        # Add buttons to layout
        self.buttonLayout.addStretch(1)
        button_widget = QtGui.QFrame(None, QtGui.QFrame.Box )
        button_widget.setLayout(self.buttonLayout)
        button_widget.setLineWidth(1)
        button_widget.setFrameShape(QtGui.QFrame.Box)
        button_widget.setFrameShadow(QtGui.QFrame.Sunken)
        self.layout().addWidget(button_widget)

        # Add calibration workspace
        self.initCalibration()
        self.initTrajectory()

    def initCalibration(self):
        # Create calibration widget
        self.calibration = Calibration()
        self.calibrationWidget = CalibrationWidget(None, self.calibration, self.machine)
        self.layout().addWidget(self.calibrationWidget)
        self.onCalibrationButtonDisabled()

    def onCalibrationButtonEnabled(self, checked):
        if not checked:
            return self.onCalibrationButtonDisabled()

        if not self.calibrationWidget.start():
            self.calibrationButton.setChecked(False)

    def onCalibrationButtonDisabled(self):
        self.calibrationWidget.abort()
        self.adjustSize()

    def initTrajectory(self):
        # Create trajectory widget
        self.trajectoryWidget = TrajectoryWidget(None, self.machine)
        self.layout().addWidget(self.trajectoryWidget)
        self.onTrajectoryButtonDisabled()

    def onTrajectoryButtonEnabled(self, checked):
        if not checked:
            return self.onTrajectoryButtonDisabled()
        self.trajectoryWidget.start()

    def onTrajectoryButtonDisabled(self):
        self.trajectoryWidget.abort()
        self.adjustSize()

    def closeEvent(self, event):
        try:
            if self.machine:
                self.machine.disconnect()
            event.accept()
        except CoreXY.ConnectException, e:
            print str(e)
            event.ignore()


if __name__ == '__main__':
    from CoreXY import CoreXY
    from SimpleMagnetToolhead import SimpleMagnetToolhead

    app = QtGui.QApplication(sys.argv)

    cxy = CoreXY()
    tool = SimpleMagnetToolhead(4,5)
    cxy.set_toolhead(tool)

    gui = MagicTableMainWindow(cxy)
    gui.show()

    sys.exit(app.exec_())