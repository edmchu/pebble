"""
6502 ASM Disassembler
"""

from emulator.instruction import Instruction
from emulator.addressing import Addressing

class Disassembler:
    def __init__(self, memory):
        self.memory = memory
        self.addressing = Addressing(memory)
        
    def read(self, address):
      return self.memory.read(address)
    
    def implied(self, address, mnemonic):

      opcode = self.read(address)

      return Instruction(
          address,
          [opcode],
          mnemonic,
          "",
      )


    def immediate(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"#$%02X" % value,
        )


    def zero_page(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"$%02X" % value,
        )


    def zero_page_x(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"$%02X,X" % value,
        )


    def zero_page_y(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"$%02X,Y" % value,
        )


    def absolute(self, address, mnemonic):

        opcode = self.read(address)
        low = self.read(address + 1)
        high = self.read(address + 2)

        absolute = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"$%04X" % absolute,
        )


    def absolute_x(self, address, mnemonic):

        opcode = self.read(address)
        low = self.read(address + 1)
        high = self.read(address + 2)

        absolute = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"$%04X,X" % absolute,
        )


    def absolute_y(self, address, mnemonic):

        opcode = self.read(address)
        low = self.read(address + 1)
        high = self.read(address + 2)

        absolute = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"$%04X,Y" % absolute,
        )


    def indirect(self, address, mnemonic):

        opcode = self.read(address)
        low = self.read(address + 1)
        high = self.read(address + 2)

        absolute = (high << 8) | low

        return Instruction(
            address,
            [opcode, low, high],
            mnemonic,
            f"($%04X)" % absolute,
        )


    def indexed_indirect(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"($%02X,X)" % value,
        )


    def indirect_indexed(self, address, mnemonic):

        opcode = self.read(address)
        value = self.read(address + 1)

        return Instruction(
            address,
            [opcode, value],
            mnemonic,
            f"($%02X),Y" % value,
        )


    def relative(self, address, mnemonic):

        opcode = self.read(address)
        offset = self.read(address + 1)

        return Instruction(
            address,
            [opcode, offset],
            mnemonic,
            f"$%02X" % offset,
        )


    def accumulator(self, address, mnemonic):

        opcode = self.read(address)

        return Instruction(
            address,
            [opcode],
            mnemonic,
            "A",
        )
        
    def disassemble(self, address):
      opcode = self.read(address)
      match opcode:

        case 0xEA:
          return self.implied(address, "NOP")

        case 0xA9:
          return self.immediate(address, "LDA")

        case 0xA2:
          return self.immediate(address, "LDX")

        case 0xA0:
          return self.immediate(address, "LDY")

        case 0x8D:
          return self.absolute(address, "STA")

        case 0x4C:
          return self.absolute(address, "JMP")

        case _:
          return Instruction(
            address,
            [opcode],
            "???",
            "",
          )
        
    def dump(self, start, end):
      pc = start
      while pc <= end:
        instruction = self.disassemble(pc)
        print(instruction)
        pc += len(instruction.bytes)