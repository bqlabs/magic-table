from Instruction.StartInstruction import StartInstruction
from Instruction.TravelInstruction import TravelInstruction
from Instruction.EndInstruction import EndInstruction

import numpy as np

__author__ = 'def'

def x(t, r = 45):
    return  r * np.cos(t)

def y(t, r = 45):
    return  r * np.sin(t)

if __name__ == '__main__':
    # Generate points of circle:
    t_array = np.arange(0, 10*np.pi, 0.1)
    points = [ ( x(t)+100, y(t)+150) for t in t_array ]

    # Generate instructions
    instructions = []
    instructions.append(StartInstruction())

    #instructions.append(TravelInstruction((0,0), (100, 100)))
    for origin, dst in zip(points[:-1], points[1:]):
         instructions.append(TravelInstruction(origin, dst))

    instructions.append(EndInstruction())

    # Generate gcode
    gcode = ''
    for instruction in instructions:
        gcode += instruction.generate_code()

    with open('test.gcode', 'w') as f:
        f.write(gcode)

