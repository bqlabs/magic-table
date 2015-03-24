pronterface_path = '/home/def/Repositories/Printrun'
gcode_file = '/home/def/Desktop/gcodes/bq_logo.gcode'

import sys, time
sys.path.append(pronterface_path)

from printrun.printcore import printcore

__author__ = 'def'

def main():
    # Create printcore to drive the printer
    pc = printcore()
    time.sleep(2)
    print '[+] Connecting to device...'
    pc.connect('/dev/ttyACM0', 115200)
    time.sleep(2)
    if pc.online:
        print '[!] Connected!'
    else:
        return 1

    # Read gcode file
    print '[+] Reading gcode...'
    with open(gcode_file, 'r') as f:
        gcode = f.readlines()
    print '[!] Read!'

    # Parse gcode and send it
    for line in gcode:
        print 'Sending: ' + line[:-1]
        if line.find('; lights on') != -1:
            pc.pause()
            pc.resume()
            pc.send( "M42 P%d S%d\n" % (4, 255))
            pc.send( "M42 P%d S%d\n" % (5, 255))
            pc.send( "M42 P%d S%d\n" % (6, 255))

        elif line.find('; lights off') != -1:
            pc.pause()
            pc.resume()
            pc.send( "M42 P%d S%d\n" % (4, 0))
            pc.send( "M42 P%d S%d\n" % (5, 0))
            pc.send( "M42 P%d S%d\n" % (6, 0))
        else:
            pc.send(line, 0.1)

    pc.disconnect()

if __name__ == '__main__':
    main()