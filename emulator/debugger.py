"""
Pebble Debugger
"""


class Debugger:
    def __init__(self, emulator):
        self.emulator = emulator
        self.running = False
    
    def dump_cpu(self):
      cpu = self.emulator.cpu
      print(
        f"A:{cpu.a:02X} "
        f"X:{cpu.x:02X} "
        f"Y:{cpu.y:02X} "
        f"SP:{cpu.sp:02X} "
        f"PC:{cpu.pc:02X}"
      )
    
    def dump_rom(self):
      self.emulator.disassembler.dump(
        0x8000,
        0x8010,
    )
    
    def current_instruction(self):
      instruction = self.emulator.disassembler.disassemble(
          self.emulator.cpu.pc
      )
      print("→", instruction)
      
    def step(self):
      self.dump_cpu()
      self.current_instruction()
      self.emulator.cpu.step()
      print("--------------------------")
