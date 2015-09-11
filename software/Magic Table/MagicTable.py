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
        self.buttonLayout.setAlignment(QtCore.Qt.AlignTop)
        button_widget = QtGui.QFrame(None, QtGui.QFrame.Box)
        button_widget.setLayout(self.buttonLayout)
        button_widget.setLineWidth(1)
        button_widget.setFrameShape(QtGui.QFrame.Box)
        button_widget.setFrameShadow(QtGui.QFrame.Sunken)
        self.layout().addWidget(button_widget)

        # Workspaces setup:
        self.workspaces = {}
        self.default_workspaces = [CalibrationWidget, TrajectoryWidget]

        for workspace in self.default_workspaces:
            self.addWorkspace(workspace)

    def addWorkspace(self, workpaceType):
        workspaceWidget = workpaceType(None, self.machine)
        button = QtGui.QPushButton()
        icon = QtGui.QIcon(workspaceWidget.icon)
        button.setIcon(icon)
        button.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        button.setCheckable(True)
        button.setToolTip(workspaceWidget.tooltip)
        button.toggled.connect(lambda checked, origin=workspaceWidget.name: self.onWorkspaceButtonEnabled(origin, checked))
        self.workspaces[workspaceWidget.name] = {'button':button, 'widget':workspaceWidget}
        self.buttonLayout.addWidget(button)
        self.layout().addWidget(workspaceWidget)
        self.onWorkspaceButtonDisabled(workspaceWidget.name)

    def onWorkspaceButtonEnabled(self, workspace, checked):
        if not checked:
            return self.onWorkspaceButtonDisabled(workspace)

        # Check if any of the other buttons is checked:
        for name, data in self.workspaces.iteritems():
            if name != workspace and data['button'].isChecked():
                data['widget'].pause()

        if not self.workspaces[workspace]['widget'].start():
            self.workspaces[workspace]['button'].setChecked(False)

    def onWorkspaceButtonDisabled(self, workspace):
        self.workspaces[workspace]['widget'].abort()
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