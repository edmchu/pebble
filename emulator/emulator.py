"""
The Pebble console.

This class owns every piece of emulated hardware.
"""

from emulator.memory import Memory
from emulator.video import Video
from emulator.controller import Controller
from emulator.cpu import CPU
from emulator.cartridge import Cartridge

class PebbleEmulator:
    """Represents one complete Pebble console."""

    def __init__(self):
        # Hardware
        self.cartridge = Cartridge()
        self.cartridge.load("games/test.bin")
        self.memory = Memory(self.cartridge)
        self.video = Video(self.memory)
        self.controller = Controller()
        self.cpu = CPU(self.memory)
    
    def update(self):
        self.cpu.step()
        self.video.update()
        