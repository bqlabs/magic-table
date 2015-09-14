from PySide import QtCore, QtGui

__author__ = 'def'

class WorkspaceWidget(QtGui.QWidget):

    name = ""
    icon = ""
    tooltip = ""

    def __init__(self, parent=None, machine=None):
        super(WorkspaceWidget, self).__init__(parent=parent)
        self.machine = machine

    def loadUI(self):
        raise NotImplemented

    def start(self):
        self.show()
        return True

    def pause(self):
        self.abort()

    def abort(self):
        if self.parent():
            self.hide()
            try:
                self.parent().adjustSize()
                self.parent().workspaces[self.name]['button'].setChecked(False)
            except AttributeError, e:
                print str(e)
        else:
            self.close()

    # Widget events
    def closeEvent(self, event):
        self.abort()

        if self.machine:
            if self.machine.toolhead:
                self.machine.toolhead.set_magnets_off()
                self.machine.toolhead.set_magnets_off()
            self.machine.disconnect()
        event.accept()
