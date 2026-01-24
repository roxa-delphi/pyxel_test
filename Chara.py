#
# Charater class
#


class Chara:

  def __init__(self, x, y, move_x, move_y):
    self.width       = 16	# width
    self.height      = 16	# height
    self.x           = x	# x position (upper left)
    self.y           = y	# y position (upper left)
    self.move_x      = move_x	# move every flame
    self.move_y      = move_y	# move every flame

    self.turn        = 0	# character flames
    self.res_n       = 0	# use character resource number
    self.charamove_n = 0	# use character move number

    self.isAlive     = True	# Dead or Alive

