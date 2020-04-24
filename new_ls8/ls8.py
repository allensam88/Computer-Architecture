#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from ram import RAM

cpu = CPU()
ram = RAM()

if len(sys.argv) == 2:
    program_filename = sys.argv[1]
else:
    print('Invalid entry --> please enter the program name.')
    exit()

ram.load(program_filename)
cpu.run(ram)
