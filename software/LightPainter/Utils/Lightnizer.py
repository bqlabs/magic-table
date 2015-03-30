
__author__ = 'def'

#gcode_file = '/home/def/Desktop/gcodes/bq_logo.gcode'
gcode_file = '../gear.gcode'

turn_off_cmd = "M42 P6 S0 ;turn off led\nM42 P5 S0 ;turn off led\nM42 P4 S0 ;turn off led\n"
turn_on_cmd = "M42 P6 S255 ;turn on led\nM42 P5 S255 ;turn on led\nM42 P4 S255 ;turn on led\n"

green_led_cmd = "M42 P6 S0 ;turn off led\nM42 P5 S5 ;turn on green led\nM42 P4 S0 ;turn off led\n"
red_led_cmd = "M42 P6 S0 ;turn off led\nM42 P5 S0 ;turn off led\nM42 P4 S5 ;turn on red led\n"
blue_led_cmd = "M42 P6 S5 ;turn on blue led\nM42 P5 S0 ;turn off led\nM42 P4 S0 ;turn off led\n"

start_cmd =   ["G21        ;metric values\n",
               "G90        ;absolute positioning\n",
               "M107       ;start with the fan off\n",
               "G28 Y0     ;move Y to min endstops\n",
               "G28 X0     ;move X to min endstops\n"]

def main():
    gcode = []
    new_gcode = []

    led_on = True

    with open(gcode_file, 'r') as f:
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
                new_gcode.append(blue_led_cmd)
            elif value < -2:
                new_gcode.append(green_led_cmd)
            elif value < -1:
                new_gcode.append(red_led_cmd)
            elif value < 0:
                # new_gcode.append('; lights on\n')
                new_gcode.append(turn_on_cmd)
            else:
                # new_gcode.append('; lights on\n')
                new_gcode.append(turn_off_cmd)
        else:
            new_gcode.append(line)

    with open(gcode_file+'_mod.gcode','w') as f:
        f.writelines(start_cmd + new_gcode[2:] + start_cmd)

if __name__ == '__main__':
    main()