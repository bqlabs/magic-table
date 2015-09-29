import os
import time as t

from Calibration import Calibration
from CoreXY import CoreXY
from SimpleMagnetToolhead import SimpleMagnetToolhead

from CoreXYMockup import CoreXYMockup
from SimpleMagnetToolheadMockup import SimpleMagnetToolheadMockup

__author__ = 'def'

calibration_file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'Apps',
                             'Chess', 'calibration-out.xml'))


def pick_and_place(machine, pick, place):
    print 'Move to : (%d, %d) -> (%d, %d)' % (pick[0], pick[1], place[0], place[1])
    machine.move(pick[0], pick[1])
    machine.toolhead.set_magnet(1, 'on')
    machine.move(place[0], place[1])
    machine.toolhead.set_magnet(1, 'off')

def chess_to_coord(chess, table):
    col, row = chess
    point = [0, 0]

    for key in table.keys():
        if col in key:
            point[0] = table[key][0]

        if row in key:
            point[1] = table[key][1]

    return tuple(point)


def main(machine):
    # Load calibration file
    calibration = Calibration()
    table = calibration.load_calibration_file(calibration_file)

    # Preparation:
    machine.connect()
    machine.home()

    # Movements:
    out_point = chess_to_coord('B0', table) #[0], calibration.real_points['out_white'][1])
    pick_and_place(machine, chess_to_coord('B4', table), out_point)
    t.sleep(1)
    pick_and_place(machine, chess_to_coord('B7', table), chess_to_coord('B4', table))
    t.sleep(1)

    # End
    machine.home()
    machine.disconnect()


if __name__ == '__main__':
    mockup = False

    if not mockup:
        cxy = CoreXY()
        tool = SimpleMagnetToolhead(4,5)
    else:
        cxy = CoreXYMockup()
        tool = SimpleMagnetToolheadMockup(4,5)

    cxy.set_toolhead(tool)
    main(cxy)
