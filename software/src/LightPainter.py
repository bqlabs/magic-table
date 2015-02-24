from Instruction.StartInstruction import StartInstruction
from Instruction.TravelInstruction import TravelInstruction
from Instruction.EndInstruction import EndInstruction

import numpy as np

__author__ = 'def'

class LightPainter:
    def __init__(self):
        # Configuration of the physical parameters
        #----------------------------------------------------------------------------------------------------
        # CoreXY dimensions
        self.total_length = 310
        self.total_width = 210

        # Working area (webcam field of view)
        # note: working_length and width need to be recalculated if they are to be configured externally
        self.working_upper_left = (140, 216)
        self.working_lower_right = (53, 93.10)
        self.working_length = abs( self.working_upper_left[1] - self.working_lower_right[1] )
        self.working_width = abs( self.working_upper_left[0] - self.working_lower_right[0] )

        # LED parameters:
        self.max_led_value = 255 # From 0 to 255
        self.led_resolution = 1

        # LED stepping (resolution of the real grid in mm) [this uses the working area frame of reference]
        self.x_step_resolution = 10
        self.y_step_resolution = 10

        # Image 'coordinates' (parameters)
        self.webcam_height = 640
        self.webcam_width = 480
        self.webcam_max_value = 255 # From 0 to 25

    # Functions related to changing the frame of reference of points
    def workingArea2CoreXYCoord(self, working_area_point, working_area_led_value = 0):
        """
            Changes coordinates from working area to CoreXY frame of reference
        """
        x = working_area_point[0] - (self.total_width - self.working_width) / 2.0
        y = working_area_point[1] - (self.total_length - self.working_length) / 2.0
        led_value = working_area_led_value

        return [ (x, y), led_value]

    def imageCoor2workingAreaCoor(self, image_point, pixel = 0):
        """
            Changes coordinates from working area to CoreXY frame of reference
        """
        x = image_point[1]
        y = self.working_length - image_point[0]
        new_pixel = np.floor( np.true_divide(pixel * np.true_divide(self.max_led_value, 255), self.led_resolution)) * self.led_resolution

        return [ (x, y), new_pixel]


def x(t, r = 45):
    return  r * np.cos(t)

def y(t, r = 45):
    return  r * np.sin(t)

def test1():
        # Generate points of circle:
    t_array = np.arange(0, 10*np.pi, 0.1)
    points = [ ( x(t)+100, y(t)+150) for t in t_array ]

    # Generate instructions
    instructions = []
    instructions.append(StartInstruction())

    #instructions.append(TravelInstruction((0,0), (100, 100)))
    for origin, dst in zip(points[:-1], points[1:]):
         instructions.append(TravelInstruction(origin, dst))

    instructions.append(EndInstruction())

    # Generate gcode
    gcode = ''
    for instruction in instructions:
        gcode += instruction.generate_code()

    with open('test.gcode', 'w') as f:
        f.write(gcode)

def test_coordinate_change():
    painter = LightPainter()

    # Generate points (in image space)
    point_array = []
    for row in range(480):
        for col  in range(640):
            if row % 2 == 0: # Even rows:
                point_array.append([col, row])
            else:
                point_array.append([639-col, row])

    # Transform points:
    tgt_points = []
    for point in point_array:
        tgt_points.append( painter.workingArea2CoreXYCoord(painter.imageCoor2workingAreaCoor(point)[0])[0])

    # Generate instructions
    instructions = []
    instructions.append(StartInstruction())

    for origin, dst in zip(tgt_points[:-1], tgt_points[1:]):
        # Transform points:
        instructions.append(TravelInstruction(origin, dst))

    instructions.append(EndInstruction())

    # Generate gcode
    gcode = ''
    for instruction in instructions:
        gcode += instruction.generate_code()

    with open('test.gcode', 'w') as f:
        f.write(gcode)



if __name__ == '__main__':
    #test1()
    test_coordinate_change()

