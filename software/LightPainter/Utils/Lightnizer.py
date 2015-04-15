import optparse

__author__ = 'def'

#gcode_file = '/home/def/Desktop/gcodes/bq_logo.gcode'
gcode_file = '../gear.gcode'

turn_off_cmd = "M42 P%d S0 ;turn off led\nM42 P%d S0 ;turn off led\nM42 P%d S0 ;turn off led\n"
turn_on_cmd = "M42 P%d S255 ;turn on led\nM42 P%d S255 ;turn on led\nM42 P%d S255 ;turn on led\n"

red_led_cmd = "M42 P%d S5 ;turn on red led\nM42 P%d S0 ;turn off led\nM42 P%d S0 ;turn off led\n"
green_led_cmd = "M42 P%d S0 ;turn off led\nM42 P%d S5 ;turn on green led\nM42 P%d S0 ;turn off led\n"
blue_led_cmd = "M42 P%d S0 ;turn off led\nM42 P%d S0 ;turn off led\nM42 P%d S5 ;turn on blue led\n"

start_cmd =   ["G21        ;metric values\n",
               "G90        ;absolute positioning\n",
               "M107       ;start with the fan off\n",
               "G28 Y0     ;move Y to min endstops\n",
               "G28 X0     ;move X to min endstops\n"]

def process_gcode(input_file, output_file, red_pin, green_pin, blue_pin):
    gcode = []
    new_gcode = []

    led_on = True

    with open(input_file, 'r') as f:
        gcode = f.readlines()

    for line in gcode:
        z_start = line.find('Z')
        if z_start != -1:
            z_end = line.find('F')
            if z_end != -1:
                value = float(line[z_start+1:z_end])
            else:
                value = float(line[z_start+1:])

            if value < -3:
                new_gcode.append(blue_led_cmd % (red_pin, green_pin, blue_pin))
            elif value < -2:
                new_gcode.append(green_led_cmd % (red_pin, green_pin, blue_pin))
            elif value < -1:
                new_gcode.append(red_led_cmd % (red_pin, green_pin, blue_pin))
            elif value < 0:
                # new_gcode.append('; lights on\n')
                new_gcode.append(turn_on_cmd % (red_pin, green_pin, blue_pin))
            else:
                # new_gcode.append('; lights on\n')
                new_gcode.append(turn_off_cmd % (red_pin, green_pin, blue_pin))
        else:
            new_gcode.append(line)

    with open(output_file,'w') as f:
        f.writelines(start_cmd + new_gcode[2:] + start_cmd)

if __name__ == '__main__':

    # Parse command-line parameters
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-i", "--input", dest="input_file", default="", type="string",help="Input gcode")
    parser.add_option("-o", "--output", dest="output_file", default="", type="string",help="Output file in which the result will be saved")
    parser.add_option("-r", "--red", dest="red_pin", default=4, type="int",help="Pin for the red LED")
    parser.add_option("-g", "--green", dest="green_pin", default=5, type="int",help="Pin for the green LED")
    parser.add_option("-b", "--blue", dest="blue_pin", default=6, type="int",help="Pin for the blue LED")
    (options, args) = parser.parse_args()

    red_pin = options.red_pin
    green_pin = options.green_pin
    blue_pin = options.blue_pin

    output_file = options.output_file
    input_file = options.input_file

    if not input_file:
        print "No input file was specified"
        exit(1)

    if not output_file:
        output_file = input_file+'_mod.gcode'

    process_gcode(input_file, output_file, red_pin, green_pin, blue_pin)