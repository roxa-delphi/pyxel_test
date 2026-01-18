#
#

class Chara:

  def __init__(self, x, y, move_x, move_y):
    self.width    = 16
    self.height   = 16
    self.x        = x
    self.y        = y
    self.move_x   = move_x
    self.move_y   = move_y
    self.res_num  = 0

    self.res_max  = 0
    self.res_page = []
    self.res_u    = []
    self.res_v    = []
    self.res_w    = []
    self.res_h    = []
    self.res_col  = []
    self.fire_x   = []
    self.fire_y   = []

  def add_res(self, page, u, v, w, h, col, fire_x = 0, fire_y = 0):
    self.res_page.append(page)
    self.res_u.append(u)
    self.res_v.append(v)
    self.res_w.append(w)
    self.res_h.append(h)
    self.res_col.append(col)
    self.fire_x.append(fire_x)
    self.fire_y.append(fire_y)

    self.res_max += 1


