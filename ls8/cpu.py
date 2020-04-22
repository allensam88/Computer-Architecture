"""CPU functionality."""

import sys

if len(sys.argv) == 2:
    program_filename = sys.argv[1]
else:
    print('Invalid entry --> please enter the program name.')
    exit()


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # program loads into long term random access memory (ram) first
        self.ram = [0] * 256
        # register is like a mini working memory, closer to the logic, faster
        self.register = [0] * 8
        self.pc = 0
        self.running = True
        # Program Run Codes
        self.dispatch = {}
        self.dispatch[1] = self.HLT		# 0b00000001
        self.dispatch[69] = self.PUSH  # 01000101
        self.dispatch[70] = self.POP  # 01000110
        self.dispatch[71] = self.PRN  # 0b01000111
        self.dispatch[130] = self.LDI  # 0b10000010
        self.dispatch[162] = self.MUL  # 0b10100010

    def load(self):
        """Load a program into memory."""

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
                self.ram_write(address, int(line, 2))

                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        # 	  0b10000010,	# LDI R0,8 --> load integer directly in to the register
        #     0b00000000,	# operand_a --> address pointer index 0
        #     0b00001000,	# operand_b --> value: 8
        #     0b01000111,	# PRN R0 --> print the value at operand_a address
        #     0b00000000,	# operand_a --> address pointer index 0
        #     0b00000001,	# HLT --> Halt/Stop program
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def HLT(self, inst_len):
        self.running = False

    def PUSH(self, inst_len):
        self.register[7] -= 1
        reg_num = self.ram_read(self.pc + 1)
        value = self.register[reg_num]
        address = self.register[7]
        self.ram_write(address, value)

    def POP(self, inst_len):
        sp = self.register[7]
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(sp)
        self.register[address] = value
        self.register[7] += 1

    def PRN(self, inst_len):
        address = self.ram_read(self.pc + 1)
        print("Print Value: ", self.register[address])

    def LDI(self, inst_len):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.register[address] = value

    def ADD(self, inst_len):
        value_a = self.ram_read(self.pc + 1)
        value_b = self.ram_read(self.pc + 2)
        self.alu('ADD', value_a, value_b)

    def SUB(self, inst_len):
        value_a = self.ram_read(self.pc + 1)
        value_b = self.ram_read(self.pc + 2)
        self.alu('SUB', value_a, value_b)

    def MUL(self, inst_len):
        value_a = self.ram_read(self.pc + 1)
        value_b = self.ram_read(self.pc + 2)
        self.alu('MUL', value_a, value_b)

    def DIV(self, inst_len):
        value_a = self.ram_read(self.pc + 1)
        value_b = self.ram_read(self.pc + 2)
        self.alu('DIV', value_a, value_b)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE --> PC: %02i | RAM: %03i %03i %03i | Register: " % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02i" % self.register[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        while self.running:
            instruction = self.ram[self.pc]
            inst_len = ((instruction & 0b11000000) >> 6) + 1
            # operand_a = self.ram_read(self.pc + 1)  # address
            # operand_b = self.ram_read(self.pc + 2)  # value

            if self.dispatch.get(instruction):
                # self.trace()
                self.dispatch[instruction](inst_len)
                self.trace()
            else:
                print("Unknown instruction")
                self.running = False

            self.pc += inst_len

            # LDI --> Load into Register immediately
            # if instruction == self.LDI:
            #     self.register[operand_a] = operand_b
            #     self.pc += 3

            # MUL --> Multiply two values
            # elif instruction == self.MUL:
            #     self.alu('MUL', operand_a, operand_b)
            #     self.pc += 3

            # PRN --> Print register value
            # elif instruction == self.PRN:
            #     print(self.register[operand_a])
            #     self.pc += 2

            # HLT --> Halt cpu
            # elif instruction == self.HLT:
            #     self.running = False
