ROM_SIZE = 32 * 1024

rom = bytearray([0xEA] * ROM_SIZE)   # Fill with NOPs

with open("games/test.bin", "wb") as f:
    f.write(rom)

print("Created games/test.bin")