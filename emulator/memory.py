"""
Pebble Memory
"""

from emulator.constants import RAM_SIZE

class Memory:
    """Represents the Pebble's 8 KB of RAM."""

    def __init__(self) -> None:
        self._ram = bytearray(RAM_SIZE)

    def read(self, address: int) -> int:
        """Read a byte from RAM."""
        return self._ram[address]

    def write(self, address: int, value: int) -> None:
        """Write a byte to RAM."""
        self._ram[address] = value & 0xFF