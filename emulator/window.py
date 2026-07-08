"""
Main emulator window.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect, QTimer, Qt
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
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
    def tick(self):
        self.emulator.update()
        self.update()

        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(
            QRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            self.emulator.video.image,
        )
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.emulator.controller.up = True
        elif event.key() == Qt.Key.Key_Down:
            self.emulator.controller.down = True
        elif event.key() == Qt.Key.Key_Left:
            self.emulator.controller.left = True
        elif event.key() == Qt.Key.Key_Right:
            self.emulator.controller.right = True
        elif event.key() == Qt.Key.Key_Enter:
            self.emulator.conroller.start = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.emulator.controller.up = False
        elif event.key() == Qt.Key.Key_Down:
            self.emulator.controller.down = False
        elif event.key() == Qt.Key.Key_Left:
            self.emulator.controller.left = False
        elif event.key() == Qt.Key.Key_Right:
            self.emulator.controller.right = False
        elif event.key() == Qt.Key.Key_Enter:
            self.emulator.controller.start = True