from Instruction import Instruction

__author__ = 'def'

class TravelInstruction(Instruction):
    type = 'TravelInstruction'

    def __init__(self, origin, destination, speed=100, led = (6, 5, 4)):
        self.origin = origin
        self.destination = destination
        self.speed = speed * 60 #mm/s

        self.led = led # (R, G, B)

    def generate_code(self):
        commands = "M42 P%d S0 ;turn off led\n" % self.led[0]
        commands +="M42 P%d S0 ;turn off led\n" % self.led[1]
        commands +="M42 P%d S0 ;turn off led\n" % self.led[2]
        commands +="G1 F%d X%d Y%d\n" % (self.speed, self.destination[0], self.destination[1])
        return commands

    def join(self, new_instruction):
        """
            Join two movement instructions
        """
        if self.led != new_instruction.led:
            raise Exception("Using different pins for LED: %s != %s. Instructions not compatible" % (str(self.led), str(new_instruction.led)))

        if self.speed != new_instruction.speed:
            raise Exception("Using different speeds: %d != %d. Instructions not compatible" % (self.speed, new_instruction.speed))

        if self.destination != new_instruction.origin:
            raise Exception("Not contiguous instructions: %s != %s. Instructions not compatible" % (str(self.destination), str(new_instruction.origin)))

        self.destination = new_instruction.destination