from Instruction import Instruction

__author__ = 'def'

class PaintInstruction(Instruction):
    type = 'PaintInstruction'

    def __init__(self, origin, destination, color, speed=100, led = (6, 5, 4)):
        self.origin = origin
        self.destination = destination
        self.color = color
        self.speed = speed * 60 #mm/s

        self.led = led # (R, G, B)

    def generate_code(self):
        commands  ="G1 F%d X%d Y%d\n" % (self.speed, self.origin[0], self.origin[1])
        commands +="M42 P%d S%d ;turn on led\n" % (self.led[0], self.color[2])#R
        commands +="M42 P%d S%d ;turn on led\n" % (self.led[1], self.color[1])#G
        commands +="M42 P%d S%d ;turn on led\n" % (self.led[2], self.color[0]) #B
        commands +="G1 F%d X%d Y%d\n" % (self.speed, self.destination[0], self.destination[1])
        return commands
