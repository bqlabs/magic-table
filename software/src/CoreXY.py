import serial
import time

__author__ = 'def'


class CoreXY:
    """
        Class to control the CoreXY
    """
    homing_gcode = "G21\nG90\nG28 Y0\nG28 X0\n"
    move_gcode = "G1 F%d X%d Y%d\n"
    led_gcode = "M42 P%d S%d\n"

    def __init__(self, port = "/dev/ttyACM0", baudrate = 115200,  led_pins = (6, 5, 4)):

        # CoreXY dimensions
        self.total_length = 310
        self.total_width = 210

        # Serial Port stuff
        self.port = port
        self.baudrate = baudrate
        self.serialPort = None

        # Toolhead data
        self.led_pins = led_pins

        # Buffer for incoming data
        self.buffer = ''
        self.initial_delay = 1 # seconds
        self.timeout = 5 # seconds


    # Connection-related functions:
    def connect(self):
        # Create serial port
        self.serialPort = serial.Serial()

        # Set the main parameters:
        self.serialPort.port = self.port
        self.serialPort.baudrate = self.baudrate

        # Open port
        self.serialPort.open()

        if self.serialPort.isOpen():
            # Reset connection:
            self.reset()

            # Read initial message
            time.sleep(self.initial_delay)
            self.readPort()
            print '-------Initial message--------'
            print self.buffer
            print '------------------------------'
            while self.getLastLine():
                pass
            return True
        else:
            return False

    def disconnect(self):
        self.serialPort.close()
        self.serialPort = None

    def reset(self):
        self.serialPort.setDTR(1)
        time.sleep(0.2)
        self.serialPort.setDTR(0)

    def readPort(self):
        """
            Reads a string from the serial port
        """
        while self.serialPort.inWaiting() > 0:
            self.buffer += self.serialPort.read(1)

    def getLastLine(self):
        """
            Reads a line from the buffer (and removes it from the buffer)
        """
        newline_pos = self.buffer.find('\n')
        if newline_pos != 1:
            line = self.buffer[:newline_pos]
            self.buffer = self.buffer[newline_pos+1:]
            return line
        else:
            return None

    def getPosFromBuffer(self):
        str = self.getLastLine()
        tokens = str.split(' ')

        print tokens[0][3:], tokens[1][3:]
        xpos = float(tokens[0][3:])
        ypos = float(tokens[1][3:])

        return (xpos, ypos)

    # Movement-related functions:
    def homing(self):
        n_lines = self.homing_gcode.count('\n')
        self.serialPort.write(self.homing_gcode)
        time.sleep(2)
        self.waitOk(n_lines)


    def moveAbs(self, point, speed=100):
        self.serialPort.write(self.move_gcode % (speed*60, point[0], point[1]))
        time.sleep(0.2)
        self.waitOk()



    def currentPos(self):
        self.serialPort.write("M114\n")
        time.sleep(0.2)

        self.readPort()
        print "Got: " + self.buffer
        return self.getPosFromBuffer()

    def waitOk(self, times = 1):
        # read = ''
        # while read == '' or read == ' ' or read != "ok\n":
        #     read = self.readPort()
        #     if read == "ok\n":
        #         print "Done!"
        self.readPort()

        for i in range(times):
            read = None
            init_time = time.time()
            while not read:
                if time.time() - init_time > self.timeout:
                    raise Exception('Timeout while waiting for ok #%d' % i)
                read = self.getLastLine()

            if read != 'ok\n':
                return False

        return True


    # Led-related functions:
    def setLed(self, px):
        self.serialPort.write(self.led_gcode % (self.led_pins[0], px[0]))
        self.waitOk()
        self.serialPort.write(self.led_gcode % (self.led_pins[1], px[1]))
        self.waitOk()
        self.serialPort.write(self.led_gcode % (self.led_pins[2], px[2]))
        self.waitOk()

    def ledOff(self):
        self.serialPort.write(self.led_gcode % (self.led_pins[0], 0))
        self.waitOk()
        self.serialPort.write(self.led_gcode % (self.led_pins[1], 0))
        self.waitOk()
        self.serialPort.write(self.led_gcode % (self.led_pins[2], 0))
        self.waitOk()



if __name__ == "__main__":

    # Create CoreXY
    coreXY = CoreXY()

    # Connect to CoreXY
    if not coreXY.connect():
        print "[-] Could not connect to CoreXY"
        exit(1)
    else:
        print "[+] Connected to CoreXY"

    # Homing
    # time.sleep(5)
    # print "[+] Received: " + coreXY.readPort()
    coreXY.homing()
    time.sleep(5)

    coreXY.moveAbs((210, 310), 200)
    time.sleep(5)

    coreXY.moveAbs((210/2, 310/2), 200)
    coreXY.setLed((255, 0, 255))
    coreXY.currentPos()
    time.sleep(5)

    coreXY.ledOff()
    coreXY.disconnect()
