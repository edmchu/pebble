"""
Pebble Memory
"""

from emulator.constants import (
    FRAMEBUFFER_START,
    FRAMEBUFFER_SIZE,
    ROM_START,
)


class Memory:

    def __init__(self, cartridge):

        # 8 KB total RAM
        self.ram = bytearray(8192)

        self.cartridge = cartridge

    def read(self, address):
        
        address &= 0xFFFF

        # RAM
        if address < 0x2000:
            return self.ram[address]

        # Cartridge ROM
        if address >= ROM_START:
            return self.cartridge.read(address - ROM_START)

        # Unused hardware area
        return 0

    def write(self, address, value):

        address &= 0xFFFF
        value &= 0xFF

        # RAM is writable
        if address < 0x2000:
            self.ram[address] = value

        # ROM ignores writes

    def get_framebuffer(self):

        return self.ram[
            FRAMEBUFFER_START:
            FRAMEBUFFER_START + FRAMEBUFFER_SIZE
        ]