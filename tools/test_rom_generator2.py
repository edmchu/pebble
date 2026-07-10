ROM_SIZE = 32768
ROM_START = 0x000

# Fill ROM with NOPs
rom = bytearray([0xEA] * ROM_SIZE)


def emit(*bytes_):
    global pc
    for b in bytes_:
        rom[pc - ROM_START] = b
        pc += 1


pc = ROM_START

# Write alternating bytes to $0000-$03FF
for address in range(0x0000, 0x0400):
    if address & 1:
        value = 0x1B
    else:
        value = 0xE4

    # LDA #value
    emit(0xA9, value)

    # STA address
    emit(
        0x8D,
        address & 0xFF,
        (address >> 8) & 0xFF,
    )

# JMP $8000
emit(0x4C, 0x00, 0x80)

# Write reset vector ($FFFC-$FFFD)
rom[0x7FFC] = 0x00
rom[0x7FFD] = 0x80

with open("test_rom.bin", "wb") as f:
    f.write(rom)

print("Created test_rom.bin")
print(f"Program size: {pc - ROM_START} bytes")
print(f"ROM size: {len(rom)} bytes")