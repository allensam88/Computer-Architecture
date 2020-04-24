from ram import RAM


class CPU:
    def __init__(self):
        # register is like a mini working memory, closer to the logic, faster
        self.register = [0] * 8
        self.pc = 0
        self.sp = 7
        self.register[self.sp] = 0xF4  # 244 decimal
        self.running = True
        # Program Run Codes
        self.dispatch = {}
        self.dispatch[1] = self.HLT		# 0b00000001
        self.dispatch[69] = self.PUSH  # 01000101
        self.dispatch[70] = self.POP  # 01000110
        self.dispatch[71] = self.PRN  # 0b01000111
        self.dispatch[130] = self.LDI  # 0b10000010

    def HLT(self, operand_a=None, operand_b=None):
        self.running = False

    def PUSH(self, operand_a=None, operand_b=None):
        self.register[7] -= 1
        reg_num = ram.read(self.pc + 1)
        value = self.register[reg_num]
        address = self.register[7]
        ram.write(address, value)

    def POP(self, operand_a=None, operand_b=None):
        sp = self.register[self.sp]
        address = ram.read(self.pc + 1)
        value = ram.read(sp)
        self.register[address] = value
        self.register[self.sp] += 1

    def PRN(self, operand_a, operand_b=None):
        address = ram.read(self.pc + 1)
        print("Print Value: ", self.register[address])

    def LDI(self, operand_a, operand_b):
        address = ram.read(self.pc + 1)
        value = ram.read(self.pc + 2)
        self.register[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == 162:
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE --> PC: %02i | RAM: %03i %03i %03i | Register:" % (
            self.pc,
            # self.fl,
            # self.ie,
            ram.read(self.pc),
            ram.read(self.pc + 1),
            ram.read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02i" % self.register[i], end='')

        print(" | Stack:", end='')

        for i in range(240, 244):
            print(" %02i" % ram.read(i), end='')

        print()

    def run(self, ram):
        while self.running:
            instruction = ram.read(self.pc)
            inst_len = ((instruction & 0b11000000) >> 6) + 1

            if inst_len >= 1:
                operand_a = ram.read(self.pc + 1)  # address
                # operand_a = self.ram_read()

            if inst_len >= 2:
                operand_b = ram.read(self.pc + 2)  # value
                # operand_b = self.ram_read()

            use_alu = ((instruction & 0b00100000) >> 5)
            # print(use_alu)

            if use_alu:
                self.alu(instruction, operand_a, operand_b)
            elif self.dispatch.get(instruction):
                self.dispatch[instruction](operand_a, operand_b)
                self.trace()
            else:
                print("Unknown instruction")
                self.running = False

            self.pc += inst_len
