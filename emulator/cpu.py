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
            # ---------------------
            # LDA - Load A Register
            
            case 0xA9: # Immediate #
                value = self.fetch()
                self.a = value

            case 0xA5: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a = value
            
            case 0xB5: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.reaad(address)
                self.a = value
                
            case 0xB9: # Absoulute, Y a,y
                address = (self.fetch() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value
                
            case 0xA1: # (Indirect, X) zp,x
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value      
                          
            case 0xB1: # (Indirect, Y) zp,y
                pointer = (self.fetch() + self.y) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value
                
