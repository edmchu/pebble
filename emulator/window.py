"""
Main emulator window.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect, QTimer
from emulator.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class EmulatorWindow(QWidget):

    def __init__(self, emulator):
        super().__init__()

        self.emulator = emulator

        self.setWindowTitle("Pebble Emulator")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000 // 30)
        
    def tick(self):
        self.emulator.video.update()
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(
            QRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            self.emulator.video.image,
        )