from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os
import time
from CoreXY import CoreXY
from CoreXYEventListener import CoreXYEventListener
from Calibration import Calibration
from Trajectory import Trajectory
from TrajectoryController import TrajectoryController
from WorkspaceWidget import WorkspaceWidget

__author__ = 'def'

class TrajectoryControllerThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(TrajectoryControllerThread, self).__init__(parent)
        self.trajectoryController = TrajectoryController()
        self.args = None
        self.kwargs = None

    def prepare(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.trajectoryController.followTrajectory(*self.args, **self.kwargs)
        self.args = None
        self.kwargs = None

    def askToStop(self):
        self.trajectoryController.askToStop()


class TrajectoryWidget(WorkspaceWidget, CoreXYEventListener):
    def __init__(self, parent, machine):
        super(TrajectoryWidget, self).__init__(parent, machine)
        self.name = "TrajectoryWidget"
        self.icon = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'resources', 'icons', 'format-text-direction-ltr.png')
        self.tooltip = "Trajectory workspace"
        self.machine.add_listener(self)
        self.trajectory = Trajectory()
        self.trajectory_controller = TrajectoryControllerThread()
        self.limits = None


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

        # Image-related
        self.pixmap = QtGui.QPixmap()
        self.original_rect = None

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

        # Set spinBox limits:
        float_max = sys.float_info.max
        self.stepSpinBox.setMaximum(float_max)
        self.xScaleSpinBox.setMaximum(float_max)
        self.yScaleSpinBox.setMaximum(float_max)
        self.xOffsetSpinBox.setMaximum(float_max)
        self.yOffsetSpinBox.setMaximum(float_max)
        self.stepSpinBox.setMinimum(0)
        self.xScaleSpinBox.setMinimum(0)
        self.yScaleSpinBox.setMinimum(0)
        self.xOffsetSpinBox.setMinimum(-float_max)
        self.yOffsetSpinBox.setMinimum(-float_max)

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
        self.trajectory_controller.finished.connect(self.onTrajectoryFinish)

    def update(self):
        self.updateImage()

    # def resetInputValues(self):
    #     self.stepSpinBox.setValue(1)
    #     self.xOffsetSpinBox.setValue(0)
    #     self.yOffsetSpinBox.setValue(0)
    #     self.xScaleSpinBox.setValue(1)
    #     self.yScaleSpinBox.setValue(1)

    def resetInputValues(self):
        self.stepSpinBox.setValue(20)
        self.xOffsetSpinBox.setValue(0)
        self.yOffsetSpinBox.setValue(-10)
        self.xScaleSpinBox.setValue(0.8)
        self.yScaleSpinBox.setValue(0.8)

    @staticmethod
    def _currentComboBoxIndex(combobox):
        try:
            return combobox.findText(combobox.currentText())
        except (IndexError, AttributeError) as e:
            print str(e)
            return None


    def loadImage(self, calibration):
        if calibration.image_name:
            self.pixmap.loadFromData(calibration.image, os.path.splitext(calibration.image_name)[1])
            self.original_rect = self.pixmap.rect()
            self.pixmap = self.pixmap.scaled(480, 339)
            return True
        else:
            return False

    def calculateTrajectoryFromParams(self):
            # Get data from form
            current_trajectory = self._currentComboBoxIndex(self.trajectoryComboBox)
            current_starting_point = self._currentComboBoxIndex(self.indexComboBox)
            step = self.stepSpinBox.value()
            x_scale, y_scale = self.xScaleSpinBox.value(), self.yScaleSpinBox.value()
            x_offset, y_offset = self.xOffsetSpinBox.value(), self.yOffsetSpinBox.value()

            # Transform trajectory
            try:
                discrete_trajectory = self.trajectory.get_normalized_path(current_trajectory, current_starting_point, step)
                print "Path length: %d points" % len(discrete_trajectory)
                discrete_trajectory = self.trajectory.scale(discrete_trajectory, 480*x_scale, 339*y_scale)
                discrete_trajectory = self.trajectory.translate(discrete_trajectory, x_offset, y_offset)
            except ArithmeticError, e:
                print e
                return False

            return discrete_trajectory

    def updateImage(self):
        # Load image and create scene
        scene = QtGui.QGraphicsScene()
        scene.addItem(QtGui.QGraphicsPixmapItem(self.pixmap))

        # Draw markers and trajectory if needed
        if self.trajectoryComboBox.currentText():
            discrete_trajectory = self.calculateTrajectoryFromParams()

            # Draw lines
            red_thin_pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            red_thin_pen.setWidth(1)
            for start, end in zip([discrete_trajectory[-1]]+discrete_trajectory[:-1], discrete_trajectory[1:]):
                scene.addLine(start[0], start[1], end[0], end[1], pen=red_thin_pen)

            # Draw starting point
            green_pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
            green_pen.setWidth(2)
            scene.addEllipse(int(discrete_trajectory[0][0]-2), int(discrete_trajectory[0][1]-2), 4, 4,
                                     pen=green_pen)

            # Draw the rest of the points
            red_thick_pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            red_thick_pen.setWidth(2)
            for point in discrete_trajectory[1:]:
                scene.addEllipse(int(point[0]-1), int(point[1]-1), 2, 2,
                                     pen=red_thick_pen)

        self.graphicsView.setScene(scene)
        self.graphicsView.show()

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
            # Ask the user for a file
            filename, ext = QtGui.QFileDialog.getOpenFileName(None, "Select SVG file", filter='*.svg' )

            if filename:
                try:
                    # Load image data from calibration file
                    calibration = Calibration()
                    calibration.load_zipfile(calibration_filename)
                    self.loadImage(calibration)
                except Calibration.LoadException, e:
                    QtGui.QMessageBox().critical(self, 'Error', 'Calibration file not compatible!')
                    return False

                try:
                    # Load points data from points file
                    self.limits = Calibration.load_calibration_file(points_filename)
                except Calibration.LoadException, e:
                    QtGui.QMessageBox().critical(self, 'Error', 'Points file not compatible!')
                    return False

                try:
                    # Load data from files
                    self.trajectory.load_paths_from_svg(filename)

                    # Set trajectories on controls
                    trajectory_choices = [ "Trajectory #%d" % i for i, path in enumerate(self.trajectory.paths)]
                    self.trajectoryComboBox.clear()
                    self.trajectoryComboBox.addItems(trajectory_choices)
                    self.setTrajectoryControlsEnabled(True)

                    self.update()
                except TrajectoryController.TrajectoryException, e:
                    pass

    def onStopButtonClicked(self):
        print "Stop button clicked"
        self.trajectory_controller.askToStop()

    def onRunButtonClicked(self):
        print "Run button clicked"
        self.runButton.setEnabled(False)
        self.stopButton.setEnabled(True)

        points = self.trajectory.scale(self.calculateTrajectoryFromParams(), 1/480.0, 1/339.0)
        self.trajectory_controller.prepare(points, self.machine, self.limits, delay=0.1/20*self.stepSpinBox.value())
        self.trajectory_controller.start()

    def onTrajectoryFinish(self):
        self.runButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def onTrajectorySelectedChanged(self):
        current_traj_choice = self._currentComboBoxIndex(self.trajectoryComboBox)
        start_point_choices = ["Point #%d" % i for i, element in \
                               enumerate(self.trajectory.paths[current_traj_choice])]
        self.indexComboBox.clear()
        self.indexComboBox.addItems(start_point_choices)

        self.resetInputValues()

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
        self.runButton.setEnabled(False)

    def on_home(self):
        self.runButton.setEnabled(True)

    def on_move(self, x, y):
        pass

    def abort(self):
        if self.trajectory_controller.isRunning():
            self.trajectory_controller.askToStop()

            if self.trajectory_controller.isRunning():
                i = 0
                while i < 100:
                    time.sleep(0.1)
                    i += 1
                    if self.trajectory_controller.isFinished():
                        print "Abort: Finished thread"
                        break
                else:
                    print "Terminating move thread"
                    self.trajectory_controller.terminate()

        super(TrajectoryWidget, self).abort()


if __name__ == '__main__':
    from TrajectoryController import TrajectoryController
    from CoreXY import CoreXY
    from SimpleMagnetToolhead import SimpleMagnetToolhead

    app = QtGui.QApplication(sys.argv)

    tj = TrajectoryController()
    cxy = CoreXY()
    tool = SimpleMagnetToolhead(4,5)
    cxy.set_toolhead(tool)
    cxy.connect()
    cxy.home()
    cxy.toolhead.set_magnet(0, 'on')
    cxy.toolhead.set_magnet(1, 'on')
    gui = TrajectoryWidget(None, cxy)
    gui.start()
    sys.exit(app.exec_())
