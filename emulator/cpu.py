"""
6502 CPU
"""


class CPU:
    """MOS 6502 CPU"""

    def __init__(self, memory):
        self.memory = memory
        self.reset()

    def reset(self):
        #
        # Registers
        #
        self.a = 0
        self.x = 0
        self.y = 0
        self.sp = 0xFF
        # Pebble starts executing ROM at $8000
        self.pc = 0x8000
        #
        # Processor Status
        #
        self.status = 0

    #
    # Fetch Helpers
    #

    def fetch(self):
        value = self.memory.read(self.pc)
        self.pc += 1
        return value
    def fetch_word(self):
        low = self.fetch()
        high = self.fetch()
        return (high << 8) | low
      
    #
    # CPU
    #
    def step(self):
        opcode = self.fetch()
        match opcode:
            #
            # NOP
            #
            case 0xEA:
                pass
            #
            # LDA Immediate
            #
            case 0xA9:
                self.a = self.fetch()
            #
            # LDX Immediate
            #
            case 0xA2:
                self.x = self.fetch()
            #
            # LDY Immediate
            #
            case 0xA0:
                self.y = self.fetch()
            #
            # TAX
            #
            case 0xAA:
                self.x = self.a
            #
            # TAY
            #
            case 0xA8:
                self.y = self.a
            #
            # TXA
            #
            case 0x8A:
                self.a = self.x
            #
            # TYA
            #
            case 0x98:
                self.a = self.y
            #
            # INX
            #
            case 0xE8:
                self.x = (self.x + 1) & 0xFF
            #
            # DEX
            #
            case 0xCA:
                self.x = (self.x - 1) & 0xFF
            #
            # INY
            #
            case 0xC8:
                self.y = (self.y + 1) & 0xFF
            #
            # DEY
            #
            case 0x88:
                self.y = (self.y - 1) & 0xFF
            #
            # JMP Absolute
            #
            case 0x4C:
                self.pc = self.fetch_word()
            #
            # STA Absolute
            #
            case 0x8D:
                address = self.fetch_word()
                self.memory.write(
                    address,
                    self.a,
                )
            #
            # Unknown Opcode
            #
            case _:
                print(
                    f"Opcode ${opcode:02X} not implemented."
                )
