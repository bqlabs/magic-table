from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os
from Calibration import Calibration
from CoreXY import CoreXY
from CoreXYEventListener import CoreXYEventListener

__author__ = 'def'


class CalibrationWidget(QtGui.QWidget, CoreXYEventListener):
    def __init__(self, parent, calibration, machine):
        super(CalibrationWidget, self).__init__()
        self.calibration = calibration
        self.machine = machine
        self.machine.add_listener(self)

        self.nextButton = None
        self.cancelButton = None
        self.progressBar = None
        self.targetPointLabel = None
        self.targetImageLabel = None
        self.toolheadPosLabel = None
        self.hintLabel = None
        self.graphicsView = None
        self.pixmap = QtGui.QPixmap()
        self.original_rect = None

        self.loadUI()
        self.update()

    def loadUI(self):
        # Load UI
        main_widget = load_ui(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'CalibrationWidget.ui'), self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)

        # Find references to controls
        self.nextButton = self.findChild(QtGui.QPushButton, "nextButton")
        self.cancelButton = self.findChild(QtGui.QPushButton, "cancelButton")
        self.progressBar = self.findChild(QtGui.QProgressBar, "progressBar")
        self.targetPointLabel = self.findChild(QtGui.QLabel, "targetPointLabel")
        self.targetImageLabel = self.findChild(QtGui.QLabel, "targetImageLabel")
        self.toolheadPosLabel = self.findChild(QtGui.QLabel, "toolheadPosLabel")
        self.hintLabel = self.findChild(QtGui.QLabel, "hintLabel")
        self.graphicsView = self.findChild(QtGui.QGraphicsView, "graphicsView")

        # Connect signals
        self.nextButton.clicked.connect(self.updateProgressBar)
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        self.nextButton.setEnabled(False)
        self.hintLabel.setText("Please connect to the machine to start")
        self.cancelButton.clicked.connect(self.abort)

    def update(self):
        self.updateProgressBar()
        self.updateLabels()
        self.updateImage()

    def start(self):
        # Ask the user for a file
        filename, ext = QtGui.QFileDialog.getOpenFileName(None, "Select calibration file", filter='*.zip' )

        if filename:
            # Try to open the calibration file
            try:
                self.calibration.load_zipfile(filename)
                self.calibration.start()
                self.loadImage()
                self.update()
                self.show()
                return True
            except Calibration.LoadException:
                QtGui.QMessageBox().critical(self, 'Error', 'File not compatible!')
                return False
            # except Exception, e:
            #     QtGui.QMessageBox().critical(self, 'Error', str(e))
            #     return False
        else:
            return False

    def abort(self):
        try:
            self.calibration.abort()
        except Calibration.CalibrationException, e:
            print str(e)

        if self.parent():
            self.hide()
            try:
                self.parent().adjustSize()
                self.parent().calibrationButton.setChecked(False)
            except AttributeError, e:
                print str(e)
        else:
            self.close()

    def onNextButtonClicked(self):
        # Get current pos and set it on the calibration object
        current_toohead_pos = (self.machine.x, self.machine.y)
        self.calibration.set_current_point_pos(current_toohead_pos)

        # Next point
        if not self.calibration.next():
            filename, ext = QtGui.QFileDialog.getSaveFileName(None, "Output file", filter='*.xml')

            if filename:
                self.calibration.save_calibration_file(filename)
            else:
                QtGui.QMessageBox().critical(self, 'Error', 'File not selected')

        self.update()

    def updateProgressBar(self):
        try:
            self.progressBar.setValue(self.calibration.get_progress()*100)
        except:
            self.progressBar.setValue(0)

    def updateToolheadPos(self):
        try:
            current_toolhead_pos = (self.machine.x, self.machine.y)
            self.toolheadPosLabel.setText('Current toolhead position: (%.2f, %.2f)' % current_toolhead_pos)
        except TypeError:
            self.toolheadPosLabel.setText('Current toolhead position: (?, ?)')

    def updateLabels(self):
        try:
            current_point = self.calibration.get_current_point_data()
            self.targetPointLabel.setText('Target point: %s' % current_point['name'])
            self.targetImageLabel.setText('Target image coordinates: (%.2f, %.2f)'%current_point['coordinates'])
        except Calibration.CalibrationException, e:
            self.targetPointLabel.setText('Target point: "Point"')
            self.targetImageLabel.setText('Target image coordinates: (u, v)')

        self.updateToolheadPos()

    def loadImage(self):
        if self.calibration.image_name:
            self.pixmap.loadFromData(self.calibration.image, os.path.splitext(self.calibration.image_name)[1])
            self.original_rect = self.pixmap.rect()
            self.pixmap = self.pixmap.scaled(480, 339)
            return True
        else:
            return False


    def updateImage(self):
        # Load image and create scene
        scene = QtGui.QGraphicsScene()
        scene.addItem(QtGui.QGraphicsPixmapItem(self.pixmap))

        # Draw markers
        if self.calibration.calibrating:
            current_point = self.calibration.get_current_point_data()['coordinates']
            scale_x = 480 / float(self.original_rect.width())
            scale_y = 339 / float(self.original_rect.height())

            try:
                pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                pen.setWidth(3)
                scene.addEllipse(int(current_point[0]*scale_x-15), int(current_point[1]*scale_y-15), 30, 30, \
                                 pen=pen)
            except Exception, e:
                print str(e)

        self.graphicsView.setScene(scene)
        self.graphicsView.show()

    # CoreXYEventListener interface:
    def on_connect(self):
        self.nextButton.setEnabled(False)
        self.hintLabel.setText("Please home the machine to the zero position")

    def on_disconnect(self):
        self.nextButton.setEnabled(False)
        self.hintLabel.setText("Please connect to the machine to start")

    def on_home(self):
        self.nextButton.setEnabled(True)
        self.hintLabel.setText("Please move the toolhead to the specified point")
        self.updateToolheadPos()

    def on_move(self, x, y):
        print "moved!"
        self.updateToolheadPos()


if __name__ == '__main__':
    from Calibration import Calibration
    from CoreXY import CoreXY
    from SimpleMagnetToolhead import SimpleMagnetToolhead

    app = QtGui.QApplication(sys.argv)

    calibration = Calibration()
    cxy = CoreXY()
    tool = SimpleMagnetToolhead(4,5)
    cxy.set_toolhead(tool)
    gui = CalibrationWidget(None, calibration, cxy)
    gui.start()
    sys.exit(app.exec_())