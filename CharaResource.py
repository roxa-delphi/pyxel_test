#
# Caharacter Move class
#

from CharaMove import CharaMove

class CharaResource:

  num = 0

  def __init__(self):
    self.res_max   = 0		# number of character resources
    self.res_page  = []		# character resource pages
    self.res_u     = []		# character resource u
    self.res_v     = []		# character resource v
    self.res_w     = []		# character resource w
    self.res_h     = []		# character resource h
    self.res_col   = []		# character resource color
    self.fire_x    = []		# fire point
    self.fire_y    = []		# fire point
    self.hita_llx  = []		# hit area
    self.hita_lly  = []		# hit area
    self.hita_urx  = []		# hit area
    self.hita_ury  = []		# hit area
    self.burn_max  = 0		# number of burn resources
    self.burn_page = []		# burn resource pages
    self.burn_u    = []		# burn resource u
    self.burn_v    = []		# burn resource v
    self.burn_w    = []		# burn resource w
    self.burn_h    = []		# burn resource h
    self.burn_col  = []		# burn resource color

    self.charamove_num = 0	# number of character moving
    self.charamove     = None	# character move list

  # add resources
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

  # add hit area
  def add_hita(self, llx, lly, urx, ury):
    self.hita_llx.append(llx)
    self.hita_lly.append(lly)
    self.hita_urx.append(urx)
    self.hita_ury.append(ury)

  # add character move list
  def add_action(self, m_x, m_y, attack):
    self.charamove     = CharaMove(m_x, m_y, attack)
    self.charamove_num = len(m_x)

  def add_burn(self, page, u, v, w, h, col):
    self.burn_page.append(page)
    self.burn_u.append(u)
    self.burn_v.append(v)
    self.burn_w.append(w)
    self.burn_h.append(h)
    self.burn_col.append(col)
    self.burn_max += 1

