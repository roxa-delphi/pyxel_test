#

from CharaMove import CharaMove

class CharaResource:

  num = 0

  def __init__(self):
    self.res_max   = 0
    self.res_page  = []
    self.res_u     = []
    self.res_v     = []
    self.res_w     = []
    self.res_h     = []
    self.res_col   = []
    self.fire_x    = []
    self.fire_y    = []
    self.hita_llx  = []
    self.hita_lly  = []
    self.hita_urx  = []
    self.hita_ury  = []
    self.burn_max  = 0
    self.burn_page = []
    self.burn_u    = []
    self.burn_v    = []
    self.burn_w    = []
    self.burn_h    = []
    self.burn_col  = []

    self.charamove_num = 0
    self.charamove     = None

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

  def add_hita(self, llx, lly, urx, ury):
    self.hita_llx.append(llx)
    self.hita_lly.append(lly)
    self.hita_urx.append(urx)
    self.hita_ury.append(ury)

  def add_action(self, m_x, m_y):
    self.charamove     = CharaMove(m_x, m_y)
    self.charamove_num = len(m_x)

  def add_burn(self, page, u, v, w, h, col):
    self.burn_page.append(page)
    self.burn_u.append(u)
    self.burn_v.append(v)
    self.burn_w.append(w)
    self.burn_h.append(h)
    self.burn_col.append(col)
    self.burn_max += 1

