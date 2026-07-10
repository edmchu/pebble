"""
6502 Addressing Modes

Used by the disassembler to decode instruction operands.
"""

from emulator.instruction import Instruction


class Addressing:

    def __init__(self, memory):
        self.memory = memory

    def read(self, address):
        return self.memory.read(address)

    #
    # Implied
    #

    def implied(self, address, mnemonic):

        opcode = self.read(address)

        return Instruction(
            address,
            [opcode],
            mnemonic,
            "",
        )

    #
    # Accumulator
    #

    def accumulator(self, address, mnemonic):

        opcode = self.read(address)

        return Instruction(
            address,
            [opcode],
            mnemonic,
            "A",
        )

    #
    # Immediate
    #

    def immediate(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"#$%02X" % value,
        )

    #
    # Zero Page
    #

    def zero_page(self, address, mnemonic):

        opcode = self.read(address)
        operand = self.read(address + 1)

        return Instruction(
            address,
            [opcode, operand],
            mnemonic,
            f"$%02X" % operand,
        )

    #
    # Zero Page,X
    #

    def zero_page_x(self, address, mnemonic):

        opcode = self.read(address)
        operand = self.read(address + 1)

        return Instruction(
            address,
            [opcode, operand],
            mnemonic,
            f"$%02X,X" % operand,
        )

    #
    # Zero Page,Y
    #

    def zero_page_y(self, address, mnemonic):

        opcode = self.read(address)
        operand = self.read(address + 1)

        return Instruction(
            address,
            [opcode, operand],
            mnemonic,
            f"$%02X,Y" % operand,
        )

    #
    # Absolute
    #

    def absolute(self, address, mnemonic):

        opcode = self.read(address)

        low = self.read(address + 1)
        high = self.read(address + 2)

        operand = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"$%04X" % operand,
        )

    #
    # Absolute,X
    #

    def absolute_x(self, address, mnemonic):

        opcode = self.read(address)

        low = self.read(address + 1)
        high = self.read(address + 2)

        operand = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"$%04X,X" % operand,
        )

    #
    # Absolute,Y
    #

    def absolute_y(self, address, mnemonic):

        opcode = self.read(address)

        low = self.read(address + 1)
        high = self.read(address + 2)

        operand = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"$%04X,Y" % operand,
        )

    #
    # Indirect
    #

    def indirect(self, address, mnemonic):

        opcode = self.read(address)

        low = self.read(address + 1)
        high = self.read(address + 2)

        operand = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"(${operand:04X})",
        )

    #
    # Indexed Indirect
    #

    def indexed_indirect(self, address, mnemonic):

        opcode = self.read(address)
        operand = self.read(address + 1)

        return Instruction(
            address,
            [opcode, operand],
            mnemonic,
            f"(${operand:02X},X)",
        )

    #
    # Indirect Indexed
    #

    def indirect_indexed(self, address, mnemonic):

        opcode = self.read(address)
        operand = self.read(address + 1)

        return Instruction(
            address,
            [opcode, operand],
            mnemonic,
            f"(${operand:02X}),Y",
        )

    #
    # Relative
    #

    def relative(self, address, mnemonic):

        opcode = self.read(address)
        offset = self.read(address + 1)

        return Instruction(
            address,
            [opcode, offset],
            mnemonic,
            f"${offset:02X}",
        )