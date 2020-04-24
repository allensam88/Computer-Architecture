class RAM:
    def __init__(self):
        self.ram = [0] * 256

    def read(self, address):
        return self.ram[address]

    def write(self, address, value):
        self.ram[address] = value

    def load(self, program_filename):
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
