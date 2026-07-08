import sys
from PySide6.QtWidgets import QApplication
from emulator.emulator import PebbleEmulator
from emulator.window import EmulatorWindow
from emulator.cartridge import Cartridge

def main():
    app = QApplication(sys.argv)
    pebble = PebbleEmulator()
    window = EmulatorWindow(pebble)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()