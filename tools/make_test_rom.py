"""
Creates a test ROM for the Pebble emulator.
"""

ROM_SIZE = 32 * 1024

rom = bytearray([0xEA] * ROM_SIZE)   # Fill entire ROM with NOPs

# Program starts at $8000


with open("games/test.bin", "wb") as file:
    file.write(rom)

print("Created games/test.bin")