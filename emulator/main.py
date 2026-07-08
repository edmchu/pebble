from emulator.memory import Memory

memory = Memory()

memory.write(0, 123)

print(memory.read(0))