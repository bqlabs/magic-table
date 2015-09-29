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


def pick_and_place(machine, pick, place, v_pick=150, v_place=80):
    print 'Move to : (%d, %d) -> (%d, %d)' % (pick[0], pick[1], place[0], place[1])
    machine.move(pick[0], pick[1], v_pick)
    machine.toolhead.set_magnet(1, 'on')
    machine.move(place[0], place[1], v_place)
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
    # --------------------------------------------------------------------------------------
    # Setup initial configuration
    setup_movements = [('A1', 'B4'), ('A8', 'B7'), ('H8', 'E6'), ('D1', 'D2')]
    for origin, destination in setup_movements:
        pick_and_place(machine, chess_to_coord(origin, table), chess_to_coord(destination, table))
        t.sleep(5)
    machine.home()

    # Capture attacking piece
    out_point = chess_to_coord('B0', table) #[0], calibration.real_points['out_white'][1])
    pick_and_place(machine, chess_to_coord('B4', table), out_point)
    t.sleep(1)

    # Simple movements
    movement_list = [('B7', 'B4'),
                     ('E6', 'D5'),
                     ('H1', 'H5'),
                     ('D5', 'D6'),
                     ('B4','B6'),
                     ('D6','C7'),
                     ('B6','F6'),
                     ('C7','D7'),
                     ('H5','H7'),
                     ('D7','D8'),
                     ('F6','F8')]

    for origin, destination in movement_list:
        pick_and_place(machine, chess_to_coord(origin, table), chess_to_coord(destination, table))
        t.sleep(5)
    machine.home()

    # Restore initial position
    cleanup_movements = [('H7', 'H1'), ('D2', 'D1'), ('B0', 'A1'), ('F8', 'F4'), ('D8', 'H8'), ('F4', 'A8')]
    for origin, destination in cleanup_movements:
        pick_and_place(machine, chess_to_coord(origin, table), chess_to_coord(destination, table))
        t.sleep(5)
    machine.home()

    # End
    machine.home()

    try:
        cxy.save_to_file('chess.gcode')
    except AttributeError:
        pass
    machine.disconnect()


if __name__ == '__main__':
    mockup = True

    if not mockup:
        cxy = CoreXY()
        tool = SimpleMagnetToolhead(4,5)
    else:
        cxy = CoreXYMockup()
        tool = SimpleMagnetToolheadMockup(4,5)

    cxy.set_toolhead(tool)
    try:
        main(cxy)
    except:
        cxy.disconnect()