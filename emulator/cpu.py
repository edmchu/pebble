"""
6502 CPU *

* In README.md
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
        self.running = True
        
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
        self.status = UNUSED

    #
    # Fetch Helpers
    #

    def fetch(self):
        value = self.memory.read(self.pc)
        self.pc = (self.pc + 1) & 0xFFFF
        return value

    def fetch_word(self):
        low = self.fetch()
        high = self.fetch()
        return (high << 8) | low

    #
    # Stack Helpers
    #

    def push(self, value):
        self.memory.write(0x0100 + self.sp, value & 0xFF)
        self.sp = (self.sp - 1) & 0xFF

    def pop(self):
        self.sp = (self.sp + 1) & 0xFF
        return self.memory.read(0x0100 + self.sp)

    #
    # Flag Helpers
    #

    def set_flag(self, flag, value):
        if value:
            self.status |= flag
        else:
            self.status &= ~flag
            
        self.status |= UNUSED

    def get_flag(self, flag):
        return (self.status & flag) != 0

    def update_zn(self, value):
        value &= 0xFF
        self.set_flag(ZERO, value == 0)
        self.set_flag(NEGATIVE, (value & 0x80) != 0)
        
    def adc(self, value):
        carry = 1 if self.get_flag(CARRY) else 0
        result = self.a + value + carry
        self.set_flag(CARRY, result > 0xFF)
        result8 = result & 0xFF
        overflow = (
            (~(self.a ^ value) &
            (self.a ^ result8) &
            0x80) != 0
        )
        self.set_flag(OVERFLOW, overflow)
        self.a = result8
        self.update_zn(self.a)

    def sbc(self, value):
        self.adc(value ^ 0xFF)

    def cmp(self, left, right):
        result = (left - right) & 0x1FF
        self.set_flag(CARRY, left >= right)
        self.update_zn(result & 0xFF)
        
    def branch(self, condition):
        offset = self.fetch()
        if offset >= 0x80:
            offset -= 0x100
        if condition:
            self.pc = (self.pc + offset) & 0xFFFF
            
    def read_word(self, address):
        low = self.memory.read(address)
        high = self.memorymread((address + 1) & 0xFFFF)
        return (high << 8) | low
      
    #
    # CPU
    #
    def step(self):
        opcode = self.fetch()
        match opcode:
            
            # ----------
            # JMP - Jump
            
            case 0x4C: # Absolute a
                address = self.fetch_word()
                self.pc = address
                
            case 0x6C: # Indirect (a)
                pointer = self.fetch_word()
                low = self.memory.read(pointer)
                high = self.memory.read(pointer + 1)
                address = ((high << 8) | low) & 0xFFFF
                self.pc = address
            
            # ---------------------
            # LDA - Load A Register
            
            case 0xA9: # Immediate #
                self.a = self.fetch()
                self.update_zn(self.a)

            case 0xA5: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.a = value
                self.update_zn(self.a)
            
            case 0xB5: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.a = value
                self.update_zn(self.a)
                
            case 0xAD: # Absolute a
                address = self.fetch_word()
                self.a = self.memory.read(address)
                self.update_zn(self.a)
                
            case 0xBD: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                self.a = self.memory.read(address)
                self.update_zn(self.a)
                
            case 0xB9: # Absoulute, Y a,y
                address = (self.fetch_word() + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.a = value
                self.update_zn(self.a)
                
            case 0xA1: # (Indirect, X) (zp,x)
                pointer = (self.fetch() + self.x) & 0xFF
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = ((high << 8) | low)
                address = (high << 8) | low
                value = self.memory.read(address)
                self.a = value   
                self.update_zn(self.a)   
                          
            case 0xB1: # (Indirect), Y (zp),y
                pointer = self.fetch()
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
                address = (address + self.y) & 0xFFFF
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
                address = self.fetch()
                value = self.memory.read(address)
                self.x = value
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
                
            case 0xB4: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.y = value
                self.update_zn(self.y)
                                
            case 0xAC: # Absolute a
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
                self.memory.write(address, self.y)

            # ------------------------------
            # Register Transfer Instructions
            
            # TAX A → X
            case 0xAA:
                self.x = self.a
                self.update_zn(self.x)
                
            # TXA X → A
            case 0x8A:
                self.a = self.x
                self.update_zn(self.a)
                
            # TAY A → Y
            case 0xA8:
                self.y = self.a
                self.update_zn(self.y)
                
            # TYA Y → A
            case 0x98:
                self.a = self.y
                self.update_zn(self.a)
            
            # TSX SP → X
            case 0xBA:
                self.x = self.sp
                self.update_zn(self.x)
                
            # TXS X → SP No Z/N Flags
            case 0x9A:
                self.sp = self.x
                
            # ----------------
            # Register Inc/Dec
            
            case 0xE8: # INX - Inc X
                self.x = (self.x + 1) & 0xFF
                self.update_zn(self.x)
            
            case 0xCA: # DEX - Dec X
                self.x = (self.x - 1) & 0xFF
                self.update_zn(self.x)
                
            case 0xC8: # INY - Inc Y
                self.y = (self.y + 1) & 0xFF
                self.update_zn(self.y)
            
            case 0x88: # DEY - Dec Y
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
                address = (high << 8) | low
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
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
                address = (high << 8) | low
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
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

            case 0x24: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                result = self.a & value
                self.set_flag(ZERO, result == 0)
                self.set_flag(NEGATIVE, (value & 0x80) != 0)
                self.set_flag(OVERFLOW, (value & 0x40) != 0)

            case 0x2C: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                result = self.a & value
                self.set_flag(ZERO, result == 0)
                self.set_flag(NEGATIVE, (value & 0x80) != 0)
                self.set_flag(OVERFLOW, (value & 0x40) != 0)
                
            # --------------------
            # ADC - Add With Carry
            
            case 0x69: # Immediate #
                value = self.fetch()
                self.adc(value)
                
            case 0x65: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
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
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                address = (address + self.y) & 0xFFFF
                value = self.memory.read(address)
                self.adc(value)     
                
            # -------------------------
            # SBC - Subtract With Carry
            
            case 0xE9: # Immediate #
                value = self.fetch()
                self.sbc(value)
                
            case 0xE5: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
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
                pointer = self.fetch()
                low = self.memory.read(pointer)
                high = self.memory.read((pointer + 1) & 0xFF)
                address = (high << 8) | low
                address = (address + self.y) & 0xFFFF
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
                value = (value << 1) & 0xFF
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
                self.memory.write(address, value)
                self.update_zn(value)
                
            # ---------------------------
            # LSR - Logical Shift Right
            
            case 0x4A: # Accumulator A
                self.set_flag(CARRY, (self.a & 0x01) != 0)
                self.a = (self.a >> 1) & 0xFF
                self.update_zn(self.a)
                
            case 0x46: # Zero Page zp
                address = self.fetch()
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value = (value >> 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x56: # Zero Page, X zp,x
                address = (self.fetch() + self.x) & 0xFF
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value = (value >> 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x4E: # Absolute a
                address = self.fetch_word()
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value = (value >> 1) & 0xFF
                self.memory.write(address, value)
                self.update_zn(value)
                
            case 0x5E: # Absolute, X a,x
                address = (self.fetch_word() + self.x) & 0xFFFF
                value = self.memory.read(address)
                self.set_flag(CARRY, (value & 0x01) != 0)
                value = (value >> 1) & 0xFF
                self.memory.write(address, value)
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
                address = self.fetch()
                value = self.memory.read(address)
                carry = self.get_flag(CARRY)
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
                
            # -------------------
            # Branch Instructions
            
            case 0x90: # BCC Branch if CARRY clear
                self.branch(not self.get_flag(CARRY))
            
            case 0xB0: # BCS Branch if CARRY set
                self.branch(self.get_flag(CARRY))
            
            case 0xF0: # BEQ Branch if ZERO set
                self.branch(self.get_flag(ZERO))
            
            case 0x30: # BMI Branch if NEGATIVE set
                self.branch(self.get_flag(NEGATIVE))
                
            case 0xD0: # BNE Branch if ZERO clear
                self.branch(not self.get_flag(ZERO))
                
            case 0x10: # BPL Branch if NEGATIVE clear
                self.branch(not self.get_flag(NEGATIVE))
                
            case 0x50: # BVC Branch if OVERFLOW clear
                self.branch(not self.get_flag(OVERFLOW))
                
            case 0x70: # BVS Branch if OVERFLOW set
                self.branch(self.get_flag(OVERFLOW))
                
            # ----------------
            # Stack Operations
            
            case 0x48: # PHA Push Accumulator
                self.push(self.a)
                
            case 0x68: # PLA Pull Accumulator
                self.a = self.pop()
                self.update_zn(self.a)
                
            case 0x08: # PHP Push Processor Status
                self.push(self.status | BREAK | UNUSED)
                
            case 0x28: # PLP Pull Processor Status
                self.status = self.pop()
                self.status |= UNUSED
                
            case 0x20: # JSR Jump To Subroutine
                address = self.fetch_word()
                return_address = (self.pc - 1) & 0xFFFF
                self.push((return_address >> 8) & 0xFF)
                self.push(return_address & 0xFF)
                self.pc = address
                
            case 0x60: # RTS Return From Subroutine
                low = self.pop()
                high = self.pop()
                self.pc = (((high << 8) | low) + 1) & 0xFFFF
                
            case 0x40: # RTI Return From Interrupt
                self.status = self.pop()
                self.status |= UNUSED
                low = self.pop()
                high = self.pop()
                self.pc = (high << 8) | low
            
            # --------------------------
            # Flag Flipping Instructions
            
            case 0x18: # CLC Clear CARRY Flag
                self.set_flag(CARRY, False)
                
            case 0x38: # SEC Set CARRY Flag
                self.set_flag(CARRY, True)
                
            case 0x58: # CLI Clear INTERRUPT Disable Flag
                self.set_flag(INTERRUPT, False)
                
            case 0x78: # SEI Set INTERRUPT Disable Flag
                self.set_flag(INTERRUPT, True)
                
            case 0xD8: # CLD Clear DECIMAL Mode
                self.set_flag(DECIMAL, False)
                
            case 0xF8: # SED Set DECIMAL Mode
                self.set_flag(DECIMAL, True)
                
            case 0xB8: # CLV Clear OVERFLOW Flag
                self.set_flag(OVERFLOW, False)
            
            # ------------------
            # NOP - No Operation
            
            case 0xEA: # NOP No Operation
                pass
            
            # -----------
            # BRK - Break
            
            case 0x00: # BRK Break
                self.running = False
                print(f"BRK ({opcode}) at ${self.pc}")
            
            # ---------------
            # Not Implemented
                       
            case 0x00:
                raise NotImplementedError(f"{opcode}")

