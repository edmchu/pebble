"""
Pebble Video Hardware
"""

from PySide6.QtGui import QImage, QColor
from emulator.constants import SCREEN_WIDTH, SCREEN_HEIGHT

COLORS = [
    QColor("white"),
    QColor(170, 170, 170),   # Light gray
    QColor(85, 85, 85),      # Dark gray
    QColor("black"),
]

class Video:
    """Represents the Pebble's display."""

    def __init__(self, memory):

        self.memory = memory

        self.image = QImage(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            QImage.Format.Format_RGB32,
        )
        self.clear()
        
    def update(self):
        framebuffer = self.memory.get_framebuffer()
        self.clear()
        for i, byte in enumerate(framebuffer):
            row = i // 16
            column = (i % 16) * 4
            pixels = self.decode_byte(byte)
            for offset, color_index in enumerate(pixels):
                self.set_pixel(column + offset, row, COLORS[color_index])
        
    def decode_byte(self, byte):
        return[
            (byte >> 6) & 0x03,
            (byte >> 4) & 0x03,
            (byte >> 2) & 0x03,
            (byte) & 0x03]
        
    def set_pixel(self, x, y, color):
      if not (0 <= x < SCREEN_WIDTH):
        return
      if not (0 <= y < SCREEN_HEIGHT):
          return
      self.image.setPixelColor(x, y, color)
        
    def clear(self, color=QColor("white")):
        """Fill Screen"""
        self.image.fill(color)
        