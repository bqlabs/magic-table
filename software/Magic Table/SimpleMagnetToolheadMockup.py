from SimpleMagnetToolhead import SimpleMagnetToolhead

__author__ = 'def'


class SimpleMagnetToolheadMockup(SimpleMagnetToolhead):
    def __init__(self, *args):
        self.command_storage = None
        self.type = 'SimpleMagnetMockup'
        self.magnets = []

        for arg in args:
            self.add_magnet(arg)

    def set_magnet(self, id, status):
        try:
            # Get value equivalent to the selected status
            if status == 'on':
                value = 255
            elif status == 'off':
                value = 0
            else:
                raise AttributeError('Status %s not supported for magnet %d' % (str(status), id))

            # Get corresponding pin
            pin = self.magnets[id]['pin']

            # Send command
            self.command_storage.append('M42 P%d S%d\n' % (pin, value))

            # Change internal status
            self.magnets[id]['status'] = status

        except IndexError:
            raise IndexError('Error: magnet %d is not attached to toolhead yet.' % id)
        except AttributeError, e:
            print str(e)
            raise AttributeError('Error: Toolhead not attached to CoreXY yet.')

    def _set_comm_interface(self, interface):
        self.command_storage = interface


try:
    from PySide import QtCore, QtGui

    class SimpleMagnetToolheadMockupWidget(QtGui.QVBoxLayout):

        state_dict = {0:'off', 2:'on'}

        def __init__(self, parent, machine):
            QtGui.QVBoxLayout.__init__(self, parent)
            self.machine = machine
            self.create_ui()

        def create_ui(self):
            for i, magnet in enumerate(self.machine.toolhead.magnets):
                widget = QtGui.QCheckBox('Magnet %d' % i)
                widget.setChecked(False)
                fn = lambda state, magnet_id = i: self.machine.toolhead.set_magnet(magnet_id, self.state_dict[state])
                widget.stateChanged.connect(fn)
                self.addWidget(widget)
            button = QtGui.QPushButton('Save')
            button.clicked.connect(lambda filename='trajectory_out.gcode': self.machine.save_to_file(filename))
            self.addWidget(button)
            self.addStretch(1)

except ImportError:
    print "[Warning] PySide not installed, widget not loaded"