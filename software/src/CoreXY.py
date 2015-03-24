import serial
import time
import numpy as np

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
        self.initial_delay = 5 # seconds
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
            self.readPortWithTimeout()
            print '-------Initial message--------'
            while True:
                line = self.getLastLine()
                if line:
                    print line
                else:
                    break
            print '------------------------------'
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


    # Communications with CoreXY board
    def readPort(self):
        """
            Reads a string from the serial port
        """
        while self.serialPort.inWaiting() > 0:
            self.buffer += self.serialPort.read(1)

    def readPortWithTimeout(self):
        """
            Reads a string from the serial port, waiting for incoming data
            during self.timeout seconds
        """
        # Read data from port to buffer:
        init_time = time.time()
        self.readPort()
        while not self.buffer:
            if time.time() - init_time > self.timeout:
                raise Exception('Timeout while waiting for data')
            self.readPort()
        #print "readPortWithTimeout> Buffer contents: " + self.buffer

    def getLastLine(self):
        """
            Reads a line from the buffer (and removes it from the buffer)
        """
        newline_pos = self.buffer.find('\n')
        if newline_pos != -1:
            line = self.buffer[:newline_pos]
            self.buffer = self.buffer[newline_pos+1:]
            return line
        else:
            return None

    def getPosFromBuffer(self):
        string = 'ok'
        #while string == 'ok\n':
        while string == "ok":
            #print "String>\"" + string + "\""
            string = self.getLastLine()
            if not string:
                raise Exception("Buffer is empty")

        tokens = string.split(' ')

        try:
            #print tokens[0][3:], tokens[1][3:]
            xpos = float(tokens[0][3:])
            ypos = float(tokens[1][3:])
            return (xpos, ypos)

        except IndexError, e:
            print "IndexError: " + e.message
            print "When processing this: " + str(tokens)
            return None

    def waitOk(self, times = 1):
        # Read data from port
        self.readPortWithTimeout()

        # Check buffer contents:
        ok = True
        for i in range(times):
            read = self.getLastLine()

            if read != 'ok\n':
                ok = False

        return ok


    # Movement-related functions:
    def sendRawCommand(self, raw_command):
        # Remove comments:
        comment_begin = raw_command.find(';')
        if comment_begin != -1:
            raw_command=raw_command[:comment_begin]

        if raw_command:
            print '[Debug] Sending: ' + raw_command
            self.serialPort.write(raw_command)

            try:
                self.readPort()
            except Exception, e:
                print '[Debug] Timeout!'
        else:
            print '[Debug] Comment!'

    def homing(self):
        n_lines = self.homing_gcode.count('\n')
        self.serialPort.write(self.homing_gcode)
        self.waitOk(n_lines)

    def moveAbs(self, point, speed=100):
        self.serialPort.write(self.move_gcode % (speed*60, point[0], point[1]))
        self.waitOk()

    def realTimeMoveAbs(self, point, speed=100):
        # Get current position
        origin = self.currentPos()

        # Calculate required time for the movement:
        distance = np.linalg.norm(np.array(point) - np.array(origin))
        required_time = np.true_divide(distance, speed)
        print "realTimeMoveAbs> Required sleep: " + str(required_time) + ' seconds'

        # Send command and wait required time
        self.moveAbs(point, speed)
        time.sleep(required_time*1.7)

    def currentPos(self):
        self.serialPort.write("M114\n")
        time.sleep(1)

        self.readPortWithTimeout()
        #print "CurrentPos> Buffer contents: " + self.buffer
        return self.getPosFromBuffer()


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



def test1():
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
    points = [ (59, 208), (59, 94), (142, 94), (142, 211)]
    try:
        coreXY.homing()
        time.sleep(5)

        coreXY.realTimeMoveAbs(points[0], 200)
        coreXY.setLed((0, 255, 255))
        #time.sleep(5)

        coreXY.realTimeMoveAbs(points[2], 200)
        coreXY.ledOff()

        coreXY.realTimeMoveAbs(points[1], 200)
        coreXY.setLed((255, 0, 255))

        coreXY.realTimeMoveAbs(points[3], 200)
        coreXY.ledOff()

        coreXY.homing()

    except Exception, e:
        print "Error occured! : " + e.message
        print "Dumping buffer: " + coreXY.buffer

    finally:
        coreXY.disconnect()

def test2():
    filename = 'test.gcode'
    coreXY = CoreXY()

    # Connect to CoreXY
    if not coreXY.connect():
        print "[-] Could not connect to CoreXY"
        exit(1)
    else:
        print "[+] Connected to CoreXY"

    with open(filename, 'r') as f:
        contents = f.readlines()

    try:
        for line in contents:
            coreXY.sendRawCommand(line)
            time.sleep(0.2)

    except Exception, e:
        print "Error occured! : " + e.message
        print "Dumping buffer: " + coreXY.buffer

    finally:
        coreXY.disconnect()

if __name__ == "__main__":
    #test1()
    test2()