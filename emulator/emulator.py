"""
The Pebble console.

This class owns every piece of emulated hardware.
"""

from emulator.memory import Memory
from emulator.video import Video


class PebbleEmulator:
    """Represents one complete Pebble console."""

    def __init__(self):

        # Hardware
        self.memory = Memory()
        self.video = Video(self.memory)