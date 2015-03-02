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


    # Connection-related functions:
    def connect(self):
        # Create serial port
        self.serialPort = serial.Serial()

        # Set the main parameters:
        self.serialPort.port = self.port
        self.serialPort.baudrate = self.baudrate

        # Open port
        self.serialPort.open()

        return self.serialPort.isOpen()

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
        string = ''
        while self.serialPort.inWaiting() > 0:
            string += self.serialPort.read(1)
        return string

    # Movement-related functions:
    def homing(self):
        self.serialPort.write(self.homing_gcode)
        #print "[+] Got: " + self.readPort()
        self.waitOk()


    def moveAbs(self, point, speed=100):
        self.serialPort.write(self.move_gcode % (speed*60, point[0], point[1]))
        self.waitOk()

        # print "[+] Got: " + self.readPort()

    def currentPos(self):
        self.serialPort.write("M114\n")
        time.sleep(0.2)

        read = ''
        while read == '' or read == ' ':
            read = self.readPort()
            print read


        print "Got: " + read


    def waitOk(self):
        read = ''
        while read == '' or read == ' ' or read != "ok\n":
            read = self.readPort()
            if read == "ok\n":
                print "Done!"

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
    time.sleep(5)
    print "[+] Received: " + coreXY.readPort()
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
