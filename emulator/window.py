"""
Main emulator window.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

class EmulatorWindow(QWidget):
    """Main Pebble emulator window."""
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pebble Emulator")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(
            "background-color: white;"
        )