
__author__ = 'def'

gcode_file = '/home/def/Desktop/gcodes/bq_logo.gcode'
turn_off_cmd = "M42 P6 S0 ;turn off led\nM42 P5 S0 ;turn off led\nM42 P4 S0 ;turn off led\n"
turn_on_cmd = "M42 P6 S255 ;turn on led\nM42 P5 S255 ;turn on led\nM42 P4 S255 ;turn on led\n"
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
        if line.find('Z') != -1:
            if led_on:
                new_gcode.append(turn_off_cmd)
                led_on = False
            else:
                new_gcode.append(turn_on_cmd)
                led_off = True
        else:
            new_gcode.append(line)

    with open(gcode_file+'_mod.gcode','w') as f:
        f.writelines(start_cmd + new_gcode[2:] + start_cmd)

if __name__ == '__main__':
    main()