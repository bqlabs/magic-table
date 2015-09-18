import os, sys
import glob
import time

from CoreXY import CoreXY

__author__ = 'def'

class CoreXYMockup(CoreXY):

    def __init__(self, port = None, baudrate=None):
        super(CoreXY, self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.comm = None

        self.command_storage = []

        self.x = None
        self.y = None

        self.toolhead = None

    def connect(self):
        self._notify_listeners("connect")

    def disconnect(self):
        self._notify_listeners("disconnect")

    def reset(self):
        try:
            self.command_storage[:] = []
        except TypeError:
            pass


    # Movement
    def home(self):
        self.reset()
        self.command_storage.append(self.home_cmd)
        self.x = 0
        self.y = 0
        self._notify_listeners("home")


    def move(self, x, y, speed=None):
        if 0 <= x <= self.x_limit and 0 <= y <= self.y_limit:
            self.command_storage.append("G1 F6000 X%s Y%s\n" % (x, y))
            self.x, self.y = x, y
            self._notify_listeners("move", self.x, self.y)
        else:
            raise AttributeError("Coordinates (%.2f, %.2f) out of limits (%.2f, %.2f)"%(x, y, self.x_limit, self.y_limit))

    def move_inc(self, inc_x, inc_y, speed=None):
        new_x = self.clip(self.x + inc_x, 0, self.x_limit)
        new_y = self.clip(self.y + inc_y, 0, self.y_limit)

        self.command_storage.append("G1 F6000 X%s Y%s\n" % (new_x, new_y))
        self.x, self.y = new_x, new_y

        self._notify_listeners("move", self.x, self.y)


    def set_toolhead(self, toolhead):
        self.toolhead = toolhead
        self.toolhead._set_comm_interface(self.command_storage)


    # Mockup functions
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.writelines(self.command_storage)
        self.clear_commands()

    def clear_commands(self):
        self.reset()
