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
                
            case 0xA1: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value      
                          
            case 0xB1: # (Indirect, Y) (zp,y)
                pointer = (self.fetch() + self.y) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value
                
            # -----------------------
            # STA - Store Accumulator
            
            case 0x85: # Zero Page zp
                address = self.fetch()
                self.memory.write(address, self.a)
                
            case 0x95: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                self.memory.write(address, self.a)
                
            case 0x8D: # Absolute a
                address = self.fetch_word()
                self.memory.write(address, self.a)
                
            case 0x9D: # Absoulute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                self.memory.write(address, self.a)
                
            case 0x99: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                self.memory.write(address, self.a)
                
            case 0x81: # (Indirect,X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                self.memory.write(address, self.a)
                
            case 0x91: # (Indirect),Y (zp),y
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                address = (address +self.y) & 0xFFFF
                self.memory.write(address, self.a)
                
            # ---------------------
            # LDX - Load X Register
            
            case 0xA2: # Immediate #
                value = self.fetch()
                self.x = value
                
            case 0xA6: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.x = value
                
            case 0xB6: # Zero Page, Y zp,y
                address = self.fetch_word()
                value = self.memory.read(address)
                self.x - value
                
            case 0xAE: # Absolute a
                address = self.fetch_word()
                vlue = self.memory.read(address)
                self.x = value
                
            case 0xBE: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.x = value
                
            # ---------------------
            # LDY - Load Y Register
            
            case 0xA0: # Immediate #
                value = self.fetch()
                self.y = value
            
            case 0xA4: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.y = value
                
            case 0xB4: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.y = value
                
            case 0xBC: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.y = value
                
            # ----------------------
            # STX - Store X Register
            
            case 0x86: # Zero Page zp
                address = self.fetch()
                self.memory.write(address, self.x)
                
            case 0x96: # Zero Page, Y zp,y
                address = (self.fetch() + self.y) & 0xFF
                self.memory.write(address, self.x)
            
            case 0x8E: # Absolute a
                address = self.fetch_word()
                self.memory.write(address, self.x)
                
            # ----------------------
            # STY - Store Y Register
            
            case 0x84: # Zero Page zp
                address = self.fetch()
                self.memory.write(address, self.y)
                
            case 0x94: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                self.memory.write(address, self.y)
                
            case 0x8C: # Absolute a
                address = self.fetch_word()
                self.memory.write(address, self.y
                                  )

            # ------------------------------
            # Register Transfer Instructions
            
            # TAX A → X
            case 0xAA:
                self.x = self.a
                
            # TXA X → A
            case 0x8A:
                self.a = self.x
                
            # TAY A → Y
            case 0xA8:
                self.y = self.a
                
            # TYA Y → A
            case 0x98:
                self.a = self.y
            
            # TSX SP → X
            case 0xBA:
                self.x = self.sp
                
            # TXS X → SP No Z/N Flags
            case 0x9A:
                self.sp = self.x
                
            # ----------------
            # Register Inc/Dec
            
            # INX - Inc X
            case 0xE8:
                self.x = (self.x + 1) & 0xFF
            
            # DEX - Dec X
            case 0xCA:
                self.x = (self.x - 1) & 0xFF
                
            # INY - Inc Y
            case 0xC8:
                self.y = (self.y + 1) & 0xFF
            
            # DEY - Dec Y
            case 0x88:
                self.y = (self.y -1) & 0xFF
                
            # ----------------------
            # INC - Increment Memory
            
            case 0xE6: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                
            case 0xF6: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)

            case 0xEE: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                
            case 0xFE: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                
            # ----------------------
            # DEC - Decrement Memory
            
            case 0xC6: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                
            case 0xD6: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                
            case 0xCE: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                
            case 0xDE: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)

            # -----------------
            # AND - Logical AND

            case 0x29: # Immediate #
                value = self.fetch()
                self.a &= value

            case 0x25: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a &= value

            case 0x35: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.a &= value

            case 0x2D: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.a &= value

            case 0x3D: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.a &= value

            case 0x39: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a &= value

            case 0x21: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.a &= value

            case 0x31: # (Indirect),Y (zp),y
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low) + self.y
                value = self.memory.read(address & 0xFFFF)
                self.a &= value
