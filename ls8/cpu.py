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
        self.dispatch[1] = self.HLT
        self.dispatch[71] = self.PRN
        self.dispatch[130] = self.LDI
        # self.MUL = 162  # 0b10100010

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
                self.ram[address] = int(line, 2)

                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        # 	0b1000 0010,  # LDI R0,8 --> load integer directly in to the register
        #     0b00000000,	 # operand_a --> address pointer index 0
        #     0b00001000,	 # operand_b --> value: 8
        #     0b0100 0111,  # PRN R0 --> print the value
        #     0b00000000,	 # empty
        #     0b00000001,  # HLT --> Halt/Stop program
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def HLT(self):
        self.running = False

    def PRN(self):
        address = self.ram_read(self.pc + 1)
        print(self.register[address])
        self.pc += 2

    def LDI(self):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.register[address] = value
        self.pc += 3

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
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        while self.running:
            instruction = self.ram[self.pc]
            # inst_len = ((instruction & 0b11000000) >> 6) + 1

            # operand_a = self.ram_read(self.pc + 1)  # address
            # operand_b = self.ram_read(self.pc + 2)  # value

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

            if self.dispatch.get(instruction):
                self.dispatch[instruction]
            else:
                print("Unknown instruction")
                self.running = False

            # self.pc += inst_len
