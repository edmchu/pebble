"""
The Pebble console.

This class owns every piece of emulated hardware.
"""

from emulator.memory import Memory
from emulator.video import Video
from emulator.controller import Controller
from emulator.demo import Demo

class PebbleEmulator:
    """Represents one complete Pebble console."""

    def __init__(self):

        # Hardware
        self.memory = Memory()
        self.video = Video(self.memory)
        self.controller = Controller()
        self.demo = Demo(self.memory, self.controller)
    
    def update(self):
        self.demo.update()
        self.video.update()