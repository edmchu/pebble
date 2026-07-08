from emulator.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from PySide6.QtGui import QColor

class Graphics:
  def __init__(self, video):
    self.video = video

  def set_pixel(self, x, y, color):
      if not (0 <= x < SCREEN_WIDTH):
        return
      if not (0 <= y < SCREEN_HEIGHT):
          return
      self.image.setPixelColor(x, y, color)
        
  def clear(self, color=QColor("white")):
    """Fill Screen"""
    self.image.fill(color)
        
  def draw_horizontal_line(self, x, y, length, color):
    for i in range(0,length):
      self.set_pixel(x+i, y, color)
            
  def draw_vertical_line(self, x, y, length, color):
      for i in range(0,length):
        self.set_pixel(x, y+i, color)
          
  def draw_rectangle(self, x, y, width, height, color):
    self.draw_vertical_line(x, y, height, color)
    self.draw_vertical_line(x + width, y, height, color)
    self.draw_horizontal_line(x, y, width, color)
    self.draw_horizontal_line(x, y + height -1, width, color)
        
  def fill_rectangle(self, x, y, width, height, color):
    for i in range(y, height+y):
        for u in range(x, width+x):
            self.set_pixel(u, i, color)