from CoreXY import CoreXY
from SimpleMagnetToolhead import SimpleMagnetToolhead

import os
import ConfigParser

__author__ = 'def'


class MagicTableController(CoreXY):

    supported_toolheads = {'SimpleMagnetToolhead':SimpleMagnetToolhead}

    default_port = '/dev/ttyACM0'
    default_baudrate = 115200

    class MagicTableException(BaseException):
        pass

    def __init__(self, config_file=None):
        if config_file:
            config = ConfigParser.ConfigParser()
            config.read([os.path.expanduser(config_file)])

            try:
                port = config.get('basic', 'port')
                baudrate = config.get('basic', 'baudrate')

                super(self.__class__, self).__init__(port=port,
                                                     baudrate=baudrate)

            except ConfigParser.NoOptionError, ConfigParser.NoSectionError:
                print 'Using default values for port and baudrate'
                super(self.__class__, self).__init__(port=self.default_port,
                                                     baudrate=self.default_baudrate)

            self.set_toolhead_from_config(config_file)

        else:
            super(self.__class__, self).__init__(port=self.default_port,
                                                 baudrate=self.default_baudrate)

    def set_toolhead_from_config(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read([os.path.expanduser(config_file)])

        try:
            type = config.get('toolhead', 'type')
            pins_str = config.get('toolhead', 'pins')
            pins = [ int(pin) for pin in pins_str.split(',') ]

            toolhead = self.supported_toolheads[type](*pins)

            self.set_toolhead(toolhead)

        except ConfigParser.NoOptionError, ConfigParser.NoSectionError:
            raise MagicTableController.MagicTableException("Bad config file")


if __name__ == '__main__':
    import time

    magic_table = MagicTableController('magictable.config')

    if magic_table.connect():
        print '[ok] Connected!'
    else:
        print '[Error] Could not connect'
        exit()

    if magic_table.home():
        print '[ok] Homing!'
    else:
        print '[Error] Error while homing!'
        exit()

    magic_table.move(100, 150)
    time.sleep(2)
    if magic_table.x == 100 and magic_table.y == 150:
        print '[ok] Absolute movement successful'
    else:
        print '[Error] Error in movement instruction to (%.2f, %.2f)'%(magic_table.x, magic_table.y)

    magic_table.move_inc(10, 20)
    if magic_table.x == 110 and magic_table.y == 170:
        print '[ok] Incremental movement successful'
    else:
        print '[Error] Error in movement instruction to (%.2f, %.2f)'%(magic_table.x, magic_table.y)
    time.sleep(2)

    magic_table.home()

    # Use toolhead
    magic_table.toolhead.set_magnet(0, 'on')

    if magic_table.toolhead.magnets[0]['status'] == 'on':
        print '[ok] Magnet turned on!'
    else:
        print '[Error] Could not turn on magnet'

    time.sleep(5)
    magic_table.toolhead.set_magnet(0, 'off')

    if magic_table.toolhead.magnets[0]['status'] == 'off':
        print '[ok] Magnet turned off!'
    else:
        print '[Error] Could not turn off magnet'


    if magic_table.disconnect():
        print '[ok] Disconnected!'
    else:
        print '[Error] Could not disconnect'
        exit()