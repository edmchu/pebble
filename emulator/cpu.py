"""
6502 CPU
"""

class CPU:
  def __init__(self, memory):
    self.memory = memory
    self.reset()
    
  def reset(self):
    self.a = 0 #Accumulator
    self.x = 0 #Index register
    self.y = 0 #Index register
    self.sp = 0xFF #Stack pointer
    self.pc = 0x8000 #Program counter
    self.status = 0
    
  def fetch(self):
    value = self.memory.read(self.pc)
    self.pc += 1
    return value
  
  def step(self):
    opcode = self.fetch()
    print(hex(opcode))
  
  
  
  
  
  
  