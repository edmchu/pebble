"""
Pebble Video Hardware
"""

from PySide6.QtGui import QColor, QImage

from emulator.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Video:
    """Represents the Pebble's display."""

    def __init__(self, memory):

        self.memory = memory

        self.image = QImage(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            QImage.Format.Format_RGB32,
        )
        self.image.fill(QColor("white"))
        self.set_pixel(31, 31, QColor("black"))
        
    def set_pixel(self, x, y, color):
        self.image.setPixelColor(x, y, color)