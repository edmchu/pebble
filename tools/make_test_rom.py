"""
Creates a test ROM for the Pebble emulator.
"""

ROM_SIZE = 32 * 1024

rom = bytearray([0xEA] * ROM_SIZE)   # Fill entire ROM with NOPs

# Program starts at $8000

rom[0] = 0xA9      # LDA #$FF
rom[1] = 0xFF

rom[2] = 0x8D      # STA $0000
rom[3] = 0x00
rom[4] = 0x00

rom[5] = 0x4C      # JMP $8000
rom[6] = 0x05
rom[7] = 0x80

with open("games/test.bin", "wb") as file:
    file.write(rom)

print("Created games/test.bin")