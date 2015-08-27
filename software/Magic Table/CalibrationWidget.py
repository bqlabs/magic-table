from PySide import QtCore, QtGui
from UtilsGUI import load_ui
import sys, os
from Calibration import Calibration

__author__ = 'def'


class CalibrationWidget(QtGui.QWidget):
    def __init__(self, parent, calibration):
        super(CalibrationWidget, self).__init__()

        self.form = None
        self.calibration = calibration

        self.loadUI()
        self.update()

    def loadUI(self):
        # Load UI
        load_ui(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'CalibrationWizard.ui'), self)
        self.form = self.findChild(QtGui.QWidget)

        self.form.nextButton.clicked.connect(self.updateProgressBar)
        self.form.nextButton.clicked.connect(self.onNextButtonClicked)
        self.form.cancelButton.clicked.connect(self.abort)

    def update(self):
        self.updateProgressBar()
        self.updateLabels()

    def start(self):
        # Ask the user for a file
        filename, ext = QtGui.QFileDialog.getOpenFileName(self, "Select calibration file", filter='*.zip' )
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
            filename, ext = QtGui.QFileDialog.getSaveFileName(self, "Output file", filter='*.xml')

            if filename:
                self.calibration.save_calibration_file(filename)
            else:
                QtGui.QMessageBox().critical(self, 'Error', 'File not selected')

        self.update()

    def updateProgressBar(self):
        try:
            self.form.progressBar.setValue(self.calibration.get_progress()*100)
        except:
            self.form.progressBar.setValue(0)

    def updateLabels(self):
        try:
            current_point = self.calibration.get_current_point_data()
            self.form.targetPointLabel.setText('Target point: %s' % current_point['name'])
            self.form.targetImageLabel.setText('Target image coordinates: (%.2f, %.2f)'%current_point['coordinates'])
            self.form.toolheadPosLabel.setText('Current toolhead position: (%.2f, %.2f)' % (0,0))

        except Calibration.CalibrationException, e:
            self.form.targetPointLabel.setText('Target point: "Point"')
            self.form.targetImageLabel.setText('Target image coordinates: (u, v)')
            self.form.toolheadPosLabel.setText('Current toolhead position: (x, y)')


if __name__ == '__main__':
    from Calibration import Calibration

    app = QtGui.QApplication(sys.argv)

    calibration = Calibration()
    gui = CalibrationWidget(None, calibration)
    gui.start()
    sys.exit(app.exec_())