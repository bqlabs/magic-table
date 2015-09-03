from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os
from CoreXY import CoreXY
from CoreXYEventListener import CoreXYEventListener
from Calibration import Calibration

__author__ = 'def'

class TrajectoryWidget(QtGui.QWidget, CoreXYEventListener):
    def __init__(self, parent, machine):
        super(TrajectoryWidget, self).__init__()
        self.machine = machine
        self.machine.add_listener(self)


        # References to widgets
        self.calibrationFileButton = None
        self.calibrationFileLineEdit = None
        self.pointsFileButton = None
        self.pointsFileLineEdit = None
        self.loadButton = None
        self.graphicsView = None
        self.trajectoryComboBox = None
        self.indexComboBox = None
        self.stepSpinBox = None
        self.xScaleSpinBox = None
        self.yScaleSpinBox = None
        self.xOffsetSpinBox = None
        self.yOffsetSpinBox = None
        self.stopButton = None
        self.runButton = None

        self.loadUI()
        self.update()


    def loadUI(self):
        # Load UI file
        main_widget = load_ui(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'TrajectoryWidget.ui'), self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)

        # Find references to controls
        self.calibrationFileButton = self.findChild(QtGui.QToolButton, "calibrationFileButton")
        self.pointsFileButton = self.findChild(QtGui.QToolButton, "pointsFileButton")
        self.loadButton = self.findChild(QtGui.QPushButton, "loadButton")
        self.stopButton = self.findChild(QtGui.QPushButton, "stopButton")
        self.runButton = self.findChild(QtGui.QPushButton, "runButton")
        self.calibrationFileLineEdit = self.findChild(QtGui.QLineEdit, "calibrationFileLineEdit")
        self.pointsFileLineEdit = self.findChild(QtGui.QLineEdit, "pointsFileLineEdit")
        self.graphicsView = self.findChild(QtGui.QGraphicsView, "graphicsView")
        self.trajectoryComboBox = self.findChild(QtGui.QComboBox, "trajectoryComboBox")
        self.indexComboBox = self.findChild(QtGui.QComboBox, "indexComboBox")
        self.stepSpinBox = self.findChild(QtGui.QDoubleSpinBox, "stepSpinBox")
        self.xScaleSpinBox = self.findChild(QtGui.QDoubleSpinBox, "xScaleSpinBox")
        self.yScaleSpinBox = self.findChild(QtGui.QDoubleSpinBox, "yScaleSpinBox")
        self.xOffsetSpinBox = self.findChild(QtGui.QDoubleSpinBox, "xOffsetSpinBox")
        self.yOffsetSpinBox = self.findChild(QtGui.QDoubleSpinBox, "yOffsetSpinBox")

        # Connect signals
        self.calibrationFileButton.clicked.connect(self.onCalibrationButtonClicked)
        self.pointsFileButton.clicked.connect(self.onPointsButtonClicked)
        self.loadButton.clicked.connect(self.onLoadButtonClicked)
        self.stopButton.clicked.connect(self.onStopButtonClicked)
        self.runButton.clicked.connect(self.onRunButtonClicked)
        self.trajectoryComboBox.currentIndexChanged.connect(self.onTrajectorySelectedChanged)
        self.indexComboBox.currentIndexChanged.connect(self.updateImage)
        self.stepSpinBox.valueChanged.connect(self.updateImage)
        self.xOffsetSpinBox.valueChanged.connect(self.updateImage)
        self.yOffsetSpinBox.valueChanged.connect(self.updateImage)
        self.xScaleSpinBox.valueChanged.connect(self.updateImage)
        self.yScaleSpinBox.valueChanged.connect(self.updateImage)
        self.runButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.setTrajectoryControlsEnabled(False)

    def update(self):
        pass

    def updateImage(self):
        print "Updating image..."

    def onCalibrationButtonClicked(self):
        # Ask the user for a file
        filename, ext = QtGui.QFileDialog.getOpenFileName(None, "Select calibration file", filter='*.zip' )

        if filename:
            self.calibrationFileLineEdit.setText(filename)

    def onPointsButtonClicked(self):
        # Ask the user for a file
        filename, ext = QtGui.QFileDialog.getOpenFileName(None, "Select points file", filter='*.xml' )

        if filename:
            self.pointsFileLineEdit.setText(filename)

    def onLoadButtonClicked(self):
        calibration_filename = self.calibrationFileLineEdit.text()
        points_filename = self.pointsFileLineEdit.text()

        if calibration_filename and points_filename:
            try:
                # Load data from files

                self.setTrajectoryControlsEnabled(True)
            except TrajectoryController.TrajectoryException, e:
                pass

    def onStopButtonClicked(self):
        print "Stop button clicked"

    def onRunButtonClicked(self):
        print "Run button clicked"

    def onTrajectorySelectedChanged(self):
        print "Trajectory Selected Changed"

    def setTrajectoryControlsEnabled(self, state):
        self.graphicsView.setEnabled(state)
        self.trajectoryComboBox.setEnabled(state)
        self.indexComboBox.setEnabled(state)
        self.stepSpinBox.setEnabled(state)
        self.xScaleSpinBox.setEnabled(state)
        self.yScaleSpinBox.setEnabled(state)
        self.xOffsetSpinBox.setEnabled(state)
        self.yOffsetSpinBox.setEnabled(state)
        self.runButton.setEnabled(state)

    # CoreXYEventListener interface:
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_home(self):
        pass

    def on_move(self, x, y):
        pass

    # Widget events
    def closeEvent(self, event):
        if self.machine:
            self.machine.disconnect()
        event.accept()

if __name__ == '__main__':
    from TrajectoryController import TrajectoryController
    from CoreXY import CoreXY
    from SimpleMagnetToolhead import SimpleMagnetToolhead

    app = QtGui.QApplication(sys.argv)

    tj = TrajectoryController()
    cxy = CoreXY()
    tool = SimpleMagnetToolhead(4,5)
    cxy.set_toolhead(tool)
    gui = TrajectoryWidget(None, cxy)
    gui.show()
    sys.exit(app.exec_())
