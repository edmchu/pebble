import os

ROM_SIZE = 32768
ROM_START = 0x8000
ROM_END = 0xFFFF

rom = bytearray([0xEA] * ROM_SIZE)


def valid_address(addr):
    return ROM_START <= addr <= ROM_END


def addr_to_index(addr):
    return addr - ROM_START


def parse_hex(s):
    return int(s, 16)


def view(addr, lines=1):
    if not valid_address(addr):
        print("Address out of range.")
        return

    for l in range(lines):
        a = addr + l * 16
        if a > ROM_END:
            break

        print(f"{a:04X}: ", end="")

        for i in range(16):
            current = a + i
            if current > ROM_END:
                break

            print(f"{rom[addr_to_index(current)]:02X} ", end="")

        print()


def write(addr, data):
    if not valid_address(addr):
        print("Address out of range.")
        return

    index = addr_to_index(addr)

    for b in data:
        if index >= ROM_SIZE:
            break
        rom[index] = b
        index += 1

    print(f"Wrote {len(data)} byte(s).")


def fill(start, end, value):
    if start > end:
        start, end = end, start

    if not valid_address(start) or not valid_address(end):
        print("Address out of range.")
        return

    for a in range(start, end + 1):
        rom[addr_to_index(a)] = value

    print("Done.")


def clear():
    global rom
    rom = bytearray([0xEA] * ROM_SIZE)
    print("ROM cleared.")


def save(filename):
    with open(f"games/{filename}", "wb") as f:
        f.write(rom)

    print("Saved.")


def load(filename):
    global rom

    if not os.path.exists(f"games/{filename}"):
        print("File not found.")
        return

    with open(f"games/{filename}", "rb") as f:
        data = f.read()

    if len(data) != ROM_SIZE:
        print("ROM must be exactly 32768 bytes.")
        return

    rom = bytearray(data)
    print("Loaded.")


def help_menu():
    print("""
Commands

view ADDRESS [LINES]
write ADDRESS BYTE BYTE BYTE...
fill START END BYTE
clear
save filename.bin
load filename.bin
exit

Examples

view 8000
view 8000 4

write 8000 A9 42 8D 00 02 00

fill 8000 80FF EA

save game.bin
load game.bin
""")


print("6502 ROM Editor")
print("ROM: $8000-$FFFF (32768 bytes)")
print("Type 'help' for commands.")

while True:
    try:
        cmd = input("> ").strip().split()

        if not cmd:
            continue

        c = cmd[0].lower()

        if c == "help":
            help_menu()

        elif c == "view":
            addr = parse_hex(cmd[1])
            lines = 1 if len(cmd) == 2 else int(cmd[2])
            view(addr, lines)

        elif c == "write":
            addr = parse_hex(cmd[1])
            bytes_to_write = [parse_hex(x) for x in cmd[2:]]
            write(addr, bytes_to_write)

        elif c == "fill":
            start = parse_hex(cmd[1])
            end = parse_hex(cmd[2])
            value = parse_hex(cmd[3])
            fill(start, end, value)

        elif c == "clear":
            clear()

        elif c == "save":
            save(cmd[1])

        elif c == "load":
            load(cmd[1])

        elif c == "exit":
            break

        else:
            print("Unknown command.")

    except Exception as e:
        print("Error:", e)