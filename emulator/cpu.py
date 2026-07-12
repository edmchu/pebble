"""
6502 CPU
"""

#
# Processor Status Flags
#

CARRY     = 0x01
ZERO      = 0x02
INTERRUPT = 0x04
DECIMAL   = 0x08
BREAK     = 0x10
UNUSED    = 0x20
OVERFLOW  = 0x40
NEGATIVE  = 0x80

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
        
    def update_zn(self, value):
        value &= 0xFF
        self.set_flag(ZERO, value == 0)
        self.set_flag(NEGATIVE, (value % 0x80) != 0)

    def set_flag(self, flag, value):
        if value:
            self.status |= flag
        else:
            self.status &= ~flag
            
    def get_flag(self, flag):
        return(self.status & flag) != 0
        
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
    
    def adc(self, value):
        carry = 1 if self.get_flag(CARRY) else 0
        result = self.a + value + carry
        self.set_flag(CARRY, self.reset > 0xFF)
        result8 = result & 0xFF
        overflow = (~(self.a ^ value) & (self.a ^ result8) & 0x80) != 0
        self.set_flag(OVERFLOW, overflow)
        self.a = result8
        self.update_zn(self.a)
        
    def sbc(self, value):
        self.adc(value ^ 0xFF)
        
    def cmp(self, left, right):
        result = (left - right) & 0x1FF
        self.set_flag(CARRY, left >= right)
        self.update_zn(result & 0xFF)
      
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
                self.update_zn(self.a)

            case 0xA5: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a = value
                self.update_zn(self.a)
            
            case 0xB5: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.reaad(address)
                self.a = value
                self.update_zn(self.a)
                
            case 0xB9: # Absoulute, Y a,y
                address = (self.fetch() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value
                self.update_zn(self.a)
                
            case 0xA1: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value   
                self.update_zn(self.a)   
                          
            case 0xB1: # (Indirect, Y) (zp,y)
                pointer = (self.fetch() + self.y) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value
                self.update_zn(self.a)
                
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
                self.update_zn(self.x)
                
            case 0xA6: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.x = value
                self.update_zn(self.x)
                
            case 0xB6: # Zero Page, Y zp,y
                address = self.fetch_word()
                value = self.memory.read(address)
                self.x - value
                self.update_zn(self.x)
                
            case 0xAE: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.x = value
                self.update_zn(self.x)
                
            case 0xBE: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.x = value
                self.update_zn(self.x)
                
            # ---------------------
            # LDY - Load Y Register
            
            case 0xA0: # Immediate #
                value = self.fetch()
                self.y = value
                self.update_zn(self.y)
            
            case 0xA4: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.y = value
                self.update_zn(self.y)
                
            case 0xB4: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.y = value
                self.update_zn(self.y)
                
            case 0xBC: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.y = value
                self.update_zn(self.y)
                
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
                self.update_zn(self.a)
                
            # TXA X → A
            case 0x8A:
                self.a = self.x
                self.update_zn(self.x)
                
            # TAY A → Y
            case 0xA8:
                self.y = self.a
                self.update_zn(self.a)
                
            # TYA Y → A
            case 0x98:
                self.a = self.y
                self.update_zn(self.y)
            
            # TSX SP → X
            case 0xBA:
                self.x = self.sp
                self.update_zn(self.sp)
                
            # TXS X → SP No Z/N Flags
            case 0x9A:
                self.sp = self.x
                
            # ----------------
            # Register Inc/Dec
            
            # INX - Inc X
            case 0xE8:
                self.x = (self.x + 1) & 0xFF
                self.update_zn(self.x)
            
            # DEX - Dec X
            case 0xCA:
                self.x = (self.x - 1) & 0xFF
                self.update_zn(self.x)
                
            # INY - Inc Y
            case 0xC8:
                self.y = (self.y + 1) & 0xFF
                self.update_zn(self.y)
            
            # DEY - Dec Y
            case 0x88:
                self.y = (self.y -1) & 0xFF
                self.update_zn(self.y)
                
            # ----------------------
            # INC - Increment Memory
            
            case 0xE6: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0xF6: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)

            case 0xEE: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0xFE: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                value = (value + 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            # ----------------------
            # DEC - Decrement Memory
            
            case 0xC6: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0xD6: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0xCE: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0xDE: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                value = (value - 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)

            # -----------------
            # AND - Logical AND

            case 0x29: # Immediate #
                value = self.fetch()
                self.a &= value
                self.update_zn(self.a)

            case 0x25: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a &= value
                self.update_zn(self.a)

            case 0x35: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.a &= value
                self.update_zn(self.a)

            case 0x2D: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.a &= value
                self.update_zn(self.a)

            case 0x3D: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.a &= value
                self.update_zn(self.a)

            case 0x39: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a &= value
                self.update_zn(self.a)

            case 0x21: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.a &= value
                self.update_zn(self.a)

            case 0x31: # (Indirect),Y (zp),y
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low) + self.y
                value = self.memory.read(address & 0xFFFF)
                self.a &= value
                self.update_zn(self.a)
                
            # ----------------
            # ORA - Logical OR

            case 0x09: # Immediate #
                value = self.fetch()
                self.a |= value
                self.update_zn(self.a)

            case 0x05: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a |= value
                self.update_zn(self.a)

            case 0x15: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.a |= value
                self.update_zn(self.a)

            case 0x0D: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.a |= value
                self.update_zn(self.a)

            case 0x1D: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.a |= value
                self.update_zn(self.a)

            case 0x19: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a |= value
                self.update_zn(self.a)

            case 0x01: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.a |= value
                self.update_zn(self.a)

            case 0x11: # (Indirect),Y (zp),y
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low) + self.y
                value = self.memory.read(address & 0xFFFF)
                self.a |= value
                self.update_zn(self.a)
                
            # -----------------
            # EOR - Logical XOR

            case 0x49: # Immediate #
                value = self.fetch()
                self.a ^= value
                self.update_zn(self.a)      

            case 0x45: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a ^= value
                self.update_zn(self.a)

            case 0x55: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.a ^= value
                self.update_zn(self.a)

            case 0x4D: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.a ^= value
                self.update_zn(self.a)

            case 0x5D: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.a ^= value
                self.update_zn(self.a)

            case 0x59: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a ^= value
                self.update_zn(self.a)

            case 0x41: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.a ^= value
                self.update_zn(self.a)

            case 0x51: # (Indirect),Y (zp),y
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low) + self.y
                value = self.memory.read(address & 0xFFFF)
                self.a ^= value
                self.update_zn(self.a)
                
            # --------------
            # BIT - Bit Test
            
            case 0x24: # Zero Page
                address = self.fetch()
                value = self.memory.read(address)
                self.update_zn(value)
                # ToDo: Update V flag
                
            case 0x2C: # Absolute
                address = self.fetch_word()
                value = self.memory.read(address)
                self.update_zn(value)
                # ToDo: Update V flag
                
            # --------------------
            # ADC - Add With Carry
            
            case 0x69: # Immediate #
                value = self.fetch()
                self.adc(value)
                
            case 0x65: # Zero Page zp
                address = self.fetch()
                value - self.memory.read(address)
                self.adc(value)
                
            case 0x75: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.adc(value)
                
            case 0x6D: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.adc(value)
                
            case 0x7D: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.adc(value)
                
            case 0x79: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.adc(value)
                
            case 0x61: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.adc(value)
                
            case 0x71: # (Indirect, Y) (zp,y)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.adc(value)
                
            # -------------------------
            # SBC - Subtract With Carry
            
            case 0xE9: # Immediate #
                value = self.fetch()
                self.sbc(value)
                
            case 0xE5: # Zero Page zp
                address = self.fetch()
                value - self.memory.read(address)
                self.sbc(value)
                
            case 0xF5: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.sbc(value)
                
            case 0xED: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.sbc(value)
                
            case 0xFD: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.sbc(value)
                
            case 0xF9: # Absolute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.sbc(value)
                
            case 0xE1: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.sbc(value)
                
            case 0xF1: # (Indirect, Y) (zp,y)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.sbc(value)
                
            # -------------------------
            # CMP - Compare Accumulator

            case 0xC9: # Immediate #
                value = self.fetch()
                self.cmp(self.a, value)

            case 0xC5: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.cmp(self.a, value)

            case 0xD5: # Zero Page,X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.cmp(self.a, value)

            case 0xCD: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.cmp(self.a, value)

            case 0xDD: # Absolute,X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.cmp(self.a, value)

            case 0xD9: # Absolute,Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.cmp(self.a, value)

            case 0xC1: # (Indirect,X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.cmp(self.a, value)

            case 0xD1: # (Indirect),Y (zp),y
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.cmp(self.a, value)
                
            # ------------------------
            # CPX - Compare X Register
                
            case 0xE0: # Immediate #
                value = self.fetch()
                self.cmp(self.x, value)
                
            case 0xE4: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.cmp(self.x, value)
                
            case 0xEC: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.cmp(self.x, value)
                
            # ------------------------
            # CPY - Compare Y Register

            case 0xC0: # Immediate #
                value = self.fetch()
                self.cmp(self.y, value)
                
            case 0xC4: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.cmp(self.y, value)
            
            case 0xCC: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.cmp(self.y, value)
                
            # ---------------------------
            # ASL - Arithmetic Shift Left
            
            case 0x0A: # Accumulator A
                self.set_flag(CARRY, (self.a & 0x80) != 0)
                self.a = (self.a << 1) & 0xFF
                self.update_zn(self.a)
                
            case 0x06: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x16: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x0E: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x1E: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                self.update_zn(value)
                
            # ---------------------------
            # LSR - Arithmetic Shift Right
            
            case 0x4A: # Accumulator A
                self.set_flag(CARRY, (self.a & 0x80) != 0)
                self.a = (self.a << 1) & 0xFF
                self.update_zn(self.a)
                
            case 0x46: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x56: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x4E: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x5E: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                self.update_zn(value)
            
            # -----------------
            # ROL - Rotate Left

            case 0x2A: # Accumulator A
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (self.a & 0x80) != 0)
                self.a = (self.a << 1) & 0xFF
                if carry:
                    self.a |= 0x01
                self.update_zn(self.a)
                
            case 0x26: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                if carry:
                    value |= 0x01
                    self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x36: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                if carry:
                    value |= 0x01
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x2E: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                if carry:
                    value |= 0x01
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x3E: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x80) != 0)
                value = (value << 1) & 0xFF
                if carry:
                    value |= 0x01
                self.memory.write(address, value)
                self.update_zn(value)

            # ------------------
            # ROR - Rotate Right
            
            case 0x6A: # Accumulator A
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (self.a & 0x01) != 0)
                self.a >>= 1
                if carry:
                    self.a |= 0x80
                self.update_zn(self.a)
            
            case 0x66: # Zero Page zp
                address - self.fetch()
                value = self.memory.read(address)
                carry= self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value >>= 1
                if carry:
                    value |= 0x80
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x76: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value >>= 1
                if carry:
                    value |= 0x80
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x6E: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value >>= 1
                if carry:
                    value |= 0x80
                self.memory.write(address, value)
                self.update_zn(value)
            
            case 0x7E: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value >>= 1
                if carry:
                    value |= 0x80
                self.memory.write(address, value)
                self.update_zn(value)   
