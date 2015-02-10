from Instruction import Instruction

__author__ = 'def'

class TravelInstruction(Instruction):
    def __init__(self, origin, destination, speed=100, led = (6, 5, 4)):
        self.origin = origin
        self.destination = destination
        self.speed = speed * 60 #mm/s

        self.led = led # (R, G, B)

    def generate_code(self):
        commands = "M42 P%d S255 ;turn off led\n" % self.led[0]
        commands +="M42 P%d S0 ;turn off led\n" % self.led[1]
        commands +="M42 P%d S0 ;turn off led\n" % self.led[2]
        commands +="G1 F%d X%d Y%d\n" % (self.speed, self.destination[0], self.destination[1])
        return commands
