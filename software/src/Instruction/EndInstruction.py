from Instruction import Instruction

__author__ = 'def'

class EndInstruction(Instruction):
    def __init__(self):
        self.code = "; -- END GCODE --\n"
        self.code +="M42 P6 S0 ;turn off led\n"
        self.code +="M42 P5 S0 ;turn off led\n"
        self.code +="M42 P4 S0 ;turn off led\n"
        self.code +="G90        ;absolute positioning\n"
        self.code +="G28 Y0     ;move Y to min endstops\n"
        self.code +="G28 X0     ;move X to min endstops\n"
        self.code +='M84                         ;steppers off\n'
        self.code +='G90                         ;absolute positioning\n'
        self.code +='; -- end of END GCODE --\n'

    def generate_code(self):
        return self.code
