# 基类方法
class BasicClass():
  def __init__(self, x, y, img, width, height):
    self.x      = x
    self.y      = y
    self.img    = img
    self.height = height
    self.width  = width
  # canvas为画布
  def selfPaint(self, canvas):
    canvas.blit(self.img, (self.x, self.y))