import sys
from cpu_2 import CPU

cpu = CPU()

if len(sys.argv) == 2:
    program_filename = sys.argv[1]
else:
    print('Invalid entry --> please enter the program name.')
    exit()


class RAM:
    def __init__(self):
        self.ram = [0] * 256

    def read(self, address):
        # self.pc += 1
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

    def PUSH(self, operand_a=None, operand_b=None):
        cpu.register[cpu.sp] -= 1
        reg_num = self.read(cpu.pc + 1)
        value = cpu.register[reg_num]
        address = cpu.register[cpu.sp]
        self.write(address, value)

    def POP(self, operand_a=None, operand_b=None):
        sp = cpu.register[cpu.sp]
        address = self.read(cpu.pc + 1)
        value = self.read(sp)
        cpu.register[address] = value
        cpu.register[cpu.sp] += 1

    def load(self):
        address = 0

        # Dynamic loading with parsing to strip away comments and convert to binary:
        with open(program_filename) as f:
            for line in f:
                # remove any comment blocks
                line = line.split('#')
                line = line[0].strip()

                # ignore any extra line spaces
                if line == '':
                    continue

                # this converts the value to binary and adds to ram
                self.write(address, int(line, 2))

                address += 1
