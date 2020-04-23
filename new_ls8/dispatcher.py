from cpu import CPU
from ram import RAM

cpu = CPU()
ram = RAM()


class Dispatcher:
    def __init__(self):
        self.dispatch = {}
        self.dispatch[1] = self.HLT		# 0b00000001
        self.dispatch[69] = self.PUSH  # 01000101
        self.dispatch[70] = self.POP  # 01000110
        self.dispatch[71] = self.PRN  # 0b01000111
        self.dispatch[130] = self.LDI  # 0b10000010

    def HLT(self, operand_a=None, operand_b=None):
        self.running = False

    def PUSH(self, operand_a=None, operand_b=None):
        cpu.register[cpu.sp] -= 1
        reg_num = ram.read(cpu.pc + 1)
        value = cpu.register[reg_num]
        address = cpu.register[cpu.sp]
        ram.write(address, value)

    def POP(self, operand_a=None, operand_b=None):
        sp = cpu.register[cpu.sp]
        address = ram.read(cpu.pc + 1)
        value = ram.read(sp)
        cpu.register[address] = value
        cpu.register[cpu.sp] += 1

    def PRN(self, operand_a, operand_b=None):
        address = ram.read(cpu.pc + 1)
        print("Print Value: ", cpu.register[address])

    def LDI(self, operand_a, operand_b):
        address = ram.read(cpu.pc + 1)
        value = ram.read(cpu.pc + 2)
        cpu.register[address] = value
