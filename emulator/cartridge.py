"""
Pebble Cartridge
"""

class Cartridge:
    """Represents a 32 KB Pebble game cartridge."""

    ROM_SIZE = 32 * 1024

    def __init__(self):
        self.rom = bytearray(self.ROM_SIZE)

    def load(self, filename):
        """Load a ROM image from a .bin file."""

        with open(filename, "rb") as file:
            data = file.read()

        if len(data) != self.ROM_SIZE:
            raise ValueError(
                f"ROM must be exactly {self.ROM_SIZE} bytes "
                f"({self.ROM_SIZE // 1024} KB)."
            )

        self.rom[:] = data

    def read(self, address):
        """Read a byte from the cartridge."""

        return self.rom[address]