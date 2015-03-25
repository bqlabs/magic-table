# Import instructions
from Instruction.StartInstruction import StartInstruction
from Instruction.TravelInstruction import TravelInstruction
from Instruction.PaintInstruction import PaintInstruction
from Instruction.EndInstruction import EndInstruction

# Import iterators
from ImageIterator.RowIterator import RowIterator

# Import image transformations
from transform_image import transform_image

# Other imports
import numpy as np
import cv2

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
        self.working_upper_left = (144.30, 216.90)
        self.working_lower_right = (54.70, 91.90)

        # LED parameters:
        self.max_led_value = 30 # From 0 to 255
        self.led_resolution = 1

        # LED stepping (resolution of the real grid in mm) [this uses the working area frame of reference]
        self.x_step_resolution = 5
        self.y_step_resolution = 5

        # Generate other parameters
        #----------------------------------------------------------------------------------------------------
        self.working_length = None
        self.working_width = None
        self.src_img_height = None
        self.src_img_width = None
        self.src_img_max_value = None

        self.configure()

    # CoreXY configuration from parameters
    def configure(self):
        """
            Calculate parameters from coreXY configuration data
        """
        # Working area (webcam field of view)
        self.working_length = abs( self.working_upper_left[1] - self.working_lower_right[1] )
        self.working_width = abs( self.working_upper_left[0] - self.working_lower_right[0] )

        # Calculations for the allowed origin image (max) dimensions
        self.src_img_height = int(self.working_width / self.x_step_resolution)
        self.src_img_width = int(self.working_length / self.y_step_resolution)

    # Functions related to changing the frame of reference of points
    def workingArea2CoreXYCoord(self, working_area_point, working_area_led_value = 0):
        """
            Changes coordinates from working area to CoreXY frame of reference
        """
        x = working_area_point[0] + self.working_lower_right[0]
        y = working_area_point[1] + self.working_lower_right[1]
        led_value = working_area_led_value

        return [ (x, y), led_value]

    def imageCoor2workingAreaCoor(self, image_point, pixel = 0):
        """
            Changes coordinates from working area to CoreXY frame of reference
        """
        x = image_point[1] * self.x_step_resolution
        y = self.working_length - image_point[0] * self.y_step_resolution
        new_pixel = np.floor( np.true_divide(pixel * np.true_divide(self.max_led_value, 255), self.led_resolution)) * self.led_resolution

        return [ (x, y), new_pixel]

    # Processing a image to get the gcode
    def process_image_to_instructions(self, image):
        """
            Gets an image and processes it to generate the gcode
        """
        # Transform image to allowed dimensions
        new_image = transform_image(image, self.src_img_width, self.src_img_height, 3)
        cv2.imwrite('debug.png', new_image)

        # Create iterator(s)
        it_origin = RowIterator(new_image)
        it_dest = RowIterator(new_image)
        it_dest.next()

        # Generate instructions
        instructions = []
        instructions.append(StartInstruction())

        for (origin_point, origin_value), (dest_point, dest_value)  in zip(it_origin, it_dest):
            # Coordinate transformation for the current points:
            wa_origin_point, wa_origin_value = self.imageCoor2workingAreaCoor(origin_point, origin_value)
            abs_origin_point, abs_origin_value = self.workingArea2CoreXYCoord(wa_origin_point, wa_origin_value)

            wa_dest_point, wa_dest_value = self.imageCoor2workingAreaCoor(dest_point, dest_value)
            abs_dest_point, abs_dest_value = self.workingArea2CoreXYCoord(wa_dest_point, wa_dest_value)

            # Generate different instructions depending of color
            if sum(abs_origin_value == 0) == abs_origin_value.size:
                # Black pixel -> travel instruction
                new_instruction = TravelInstruction(abs_origin_point, abs_dest_point)

                # Try to accumulate travel instructions
                try:
                    if instructions[-1].type == 'TravelInstruction':
                        instructions[-1].join(new_instruction)
                except:
                    instructions.append(new_instruction)

            else:
                new_instruction = PaintInstruction(abs_origin_point, abs_dest_point, abs_origin_value)
                instructions.append(new_instruction)



        instructions.append(EndInstruction())

        return instructions


    def process_image_to_gcode(self, image):
        """
            Gets an image and processes it to generate the gcode
        """
        # Generate instructions
        instructions = self.process_image_to_instructions(image)

        # Generate gcode
        gcode = ''
        for instruction in instructions:
            gcode += instruction.generate_code()

        return gcode


# Test #1 : trajectory generation
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

# Test #2: coordinate change test
def test_coordinate_change():
    painter = LightPainter()

    # Testing coordinate change:
    print "Checking coordinate change..."
    # Image point: (0, 0) -> Working area: (0, painter.working_length) -> Absolute frame: (painter.working_lower_right[0], painter.working_upper_left[1])
    wa_point = painter.imageCoor2workingAreaCoor([0,0])[0]
    abs_point = painter.workingArea2CoreXYCoord([0, painter.working_length])[0]

    if wa_point[0] == 0 and wa_point[1] == painter.working_length:
        print "\tImage coordinate to working area convert is ok"
    else:
        print "\tError in image coordinate to working area convert (%f, %f) != (0, %f)" % (wa_point[0], wa_point[1], painter.working_length)

    if abs_point[0] == 53 and abs_point[1] == 216:
        print "\tWorking area to abs frame convert is ok"
    else:
        print "\tError in working area to abs frame convert (%f, %f) != (%f, %f)" % (abs_point[0], abs_point[1], painter.working_lower_right[0], painter.working_upper_left[1])


    # Generate points (in image space)
    print "Generating dummy image of max allowed dimensions: %dx%d"%(painter.src_img_width, painter.src_img_height)
    point_array = []
    for row in range(painter.src_img_height):
        for col  in range(painter.src_img_width):
            if row % 2 == 0: # Even rows:
                point_array.append([col, row])
            else:
                point_array.append([painter.src_img_width-1-col, row])

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

# Test #3: application test
def test_image_processing():
    # Load image to 'print'
    #image_to_load = 'Granger_Chart.jpg'
    image_to_load = 'pattern4.png'
    src = cv2.imread(image_to_load)

    # Create LightPainter
    painter = LightPainter()

    # Process image
    gcode = painter.process_image_to_gcode(src)

    # Write gcode to disk
    with open('test.gcode', 'w') as f:
        f.write(gcode)

if __name__ == '__main__':
    #test1()
    #test_coordinate_change()
    test_image_processing()
