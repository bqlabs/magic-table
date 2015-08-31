import os, sys
import glob
import time

pronterface_path = '/home/def/Repositories/Printrun'
sys.path.append(pronterface_path)

from printrun.printcore import printcore
from CoreXYEventListener import CoreXYEventListener

__author__ = 'def'


class CoreXY(object):
    """ Basic class to control a CoreXY with Marlin Firmware """

    class ConnectException(BaseException):
        pass

    x_limit = 200
    y_limit = 300

    home_cmd = "G28 Y0\nG28 X0\n"

    def __init__(self, port = '/dev/ttyACM0', baudrate = 115200):
        self.port = port
        self.baudrate = baudrate
        self.comm = printcore()

        self.x = None
        self.y = None

        self.toolhead = None

        self.listeners = []

    # Basic functionality (provided by the communications interface)
    def connect(self):
        if not self.comm.online:
            self.comm.connect(self.port, self.baudrate)
            time.sleep(2)
            if self.comm.online:
                for listener in self.listeners:
                    listener.on_connect()
                return True
            else:
                raise CoreXY.ConnectException('Could not connect to the device')

    def disconnect(self):
        if self.comm.online:
            self.comm.disconnect()
            time.sleep(2)
            if not self.comm.online:
                for listener in self.listeners:
                    listener.on_disconnect()
                return True
            else:
                raise CoreXY.ConnectException('Could not disconnect from the device')

    def reset(self):
        self.comm.reset()

    # Communications helper functions
    @staticmethod
    def get_available_ports():
        """scan for available ports. return a list of device names."""
        ports = []
        names = ['/dev/ttyUSB*', '/dev/ttyACM*', "/dev/tty.*", "/dev/cu.*", "/dev/rfcomm*"]

        for name in names:
            ports += glob.glob(name)

        return ports

    @staticmethod
    def get_available_baudrates():
        return ["2400", "9600", "19200", "38400", "57600", "115200", "250000"]

    # Movement
    def home(self):
        self.comm.send(self.home_cmd)
        self.x, self.y = 0, 0
        for listener in self.listeners:
            listener.on_home()
        return True

    def move(self, x, y, speed=None):
        if 0 <= x <= self.x_limit and 0 <= y <= self.y_limit:
            self.comm.send("G1 F6000 X%s Y%s\n" % (x, y))
            self.x, self.y = x, y
            for listener in self.listeners:
                listener.on_move(self.x, self.y)
        else:
            raise AttributeError("Coordinates (%.2f, .2f) out of limits (%.2f, %.2f)"%(x, y, self.x_limit, self.y_limit))

    @staticmethod
    def clip(value, min, max):
        if value < min:
            value = min
        elif value > max:
            value = max

        return value

    def move_inc(self, inc_x, inc_y, speed=None):
        new_x = self.clip(self.x + inc_x, 0, self.x_limit)
        new_y = self.clip(self.y + inc_y, 0, self.y_limit)

        self.comm.send("G1 F6000 X%s Y%s\n" % (new_x, new_y))
        self.x, self.y = new_x, new_y

        for listener in self.listeners:
            listener.on_move(self.x, self.y)

    # Toolhead functions
    def set_toolhead(self, toolhead):
        self.toolhead = toolhead
        self.toolhead._set_comm_interface(self.comm)

    # Listener functions
    def add_listener(self, listener):
        self.listeners.append(listener)


if __name__ == '__main__':

    cxy = CoreXY()

    if cxy.connect():
        print '[ok] Connected!'
    else:
        print '[Error] Could not connect'
        exit()

    if cxy.home():
        print '[ok] Homing!'
    else:
        print '[Error] Error while homing!'
        exit()

    cxy.move(100, 150)
    time.sleep(2)
    if cxy.x == 100 and cxy.y == 150:
        print '[ok] Absolute movement successful'
    else:
        print '[Error] Error in movement instruction to (%.2f, %.2f)'%(cxy.x, cxy.y)

    cxy.move_inc(10, 20)
    if cxy.x == 110 and cxy.y == 170:
        print '[ok] Incremental movement successful'
    else:
        print '[Error] Error in movement instruction to (%.2f, %.2f)'%(cxy.x, cxy.y)
    time.sleep(2)

    cxy.home()

    if cxy.disconnect():
        print '[ok] Disconnected!'
    else:
        print '[Error] Could not disconnect'
        exit()