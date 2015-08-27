from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os
from Calibration import Calibration

__author__ = 'def'


class CalibrationWidget(QtGui.QWidget):
    def __init__(self, parent, calibration):
        super(CalibrationWidget, self).__init__()
        self.calibration = calibration

        self.nextButton = None
        self.cancelButton = None
        self.progressBar = None
        self.targetPointLabel = None
        self.targetImageLabel = None
        self.toolheadPosLabel = None

        self.loadUI()
        self.update()

    def loadUI(self):
        # Load UI
        main_widget = load_ui(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'CalibrationWizard.ui'), self)
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

        # Connect signals
        self.nextButton.clicked.connect(self.updateProgressBar)
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        self.cancelButton.clicked.connect(self.abort)

    def update(self):
        self.updateProgressBar()
        self.updateLabels()

    def start(self):
        # Ask the user for a file
        filename, ext = QtGui.QFileDialog.getOpenFileName(None, "Select calibration file", filter='*.zip' )
        # filename = '/home/def/Documents/CoreXY/software/Magic Table/resources/calibration/calibration.zip'

        if filename:
            # Try to open the calibration file
            try:
                self.calibration.load_zipfile(filename)
                self.calibration.start()
                self.update()
                self.show()
                return True
            except Calibration.LoadException:
                QtGui.QMessageBox().critical(self, 'Error', 'File not compatible!')
                return False
            except Exception, e:
                QtGui.QMessageBox().critical(self, 'Error', str(e))
                return False
        else:
            return False

    def abort(self):
        try:
            self.calibration.abort()
        except Calibration.CalibrationException, e:
            print str(e)

        if self.parent():
            self.hide()
        else:
            self.close()

    def onNextButtonClicked(self):
        # Get current pos and set it on the calibration object
        current_toohead_pos = (0,0)
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

    def updateLabels(self):
        try:
            current_point = self.calibration.get_current_point_data()
            self.targetPointLabel.setText('Target point: %s' % current_point['name'])
            self.targetImageLabel.setText('Target image coordinates: (%.2f, %.2f)'%current_point['coordinates'])
            self.toolheadPosLabel.setText('Current toolhead position: (%.2f, %.2f)' % (0,0))

        except Calibration.CalibrationException, e:
            self.targetPointLabel.setText('Target point: "Point"')
            self.targetImageLabel.setText('Target image coordinates: (u, v)')
            self.toolheadPosLabel.setText('Current toolhead position: (x, y)')


if __name__ == '__main__':
    from Calibration import Calibration

    app = QtGui.QApplication(sys.argv)

    calibration = Calibration()
    gui = CalibrationWidget(None, calibration)
    gui.start()
    sys.exit(app.exec_())