class Demo:

    def __init__(self, memory, controller):
        self.memory = memory
        self.controller = controller

        self.x = 31
        self.y = 31

    def update(self):
      self.clear()
      if self.controller.left:
          self.x -= 1
      if self.controller.right:
          self.x += 1
      if self.controller.up:
          self.y -= 1
      if self.controller.down:
          self.y += 1
      self.set_pixel(self.x, self.y, 3)
    
    def set_pixel(self, x, y, color):
      byte_index = y * 16 + (x // 4)
      shift = (3 - (x % 4)) * 2
      mask = 0b11 << shift
      value = (color & 0b11) << shift
      current = self.memory.read(byte_index)
      current &= ~mask
      current |= value
      self.memory.write(byte_index, current)
      
    def clear(self):
      framebuffer = self.memory.get_framebuffer()
      for i in range(len(framebuffer)):
        self.memory.write(i, 0)
    