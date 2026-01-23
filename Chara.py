#
#



class Chara:

  def __init__(self, x, y, move_x, move_y):
    self.width       = 16
    self.height      = 16
    self.x           = x
    self.y           = y
    self.move_x      = move_x
    self.move_y      = move_y

    self.turn        = 0
    self.res_n       = 0
    self.charamove_n = 0

    self.isAlive     = True

