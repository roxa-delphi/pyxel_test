#
#

import pyxel
from Chara import Chara


class App:
  _miss_m = 10
  _cw     = 16
  _width  = 300
  _height = 200

  turn = 0

  player     = None
  p_miss_max = 6
  p_miss_f   = []
  p_miss     = []


  def __init__(self):

    # player settings
    self.player = Chara(40, 80, 8, 8)
    self.player.add_res(0, 0, 16, 16, 16, 0, 16, 7)
    self.player.add_res(0, 16, 16, 16, 16, 0, 16, 7)

    # player missile settings
    for i in range(0, self.p_miss_max):
      self.p_miss_f.append(False)
      self.p_miss.append(Chara(0, 0, 10, 0))
      self.p_miss[i].add_res(0, 38, 23, 4, 2, 12)


    pyxel.init(self._width, self._height, title="test", fps=15)
    pyxel.load("assets/test.pyxres")
    pyxel.run(self.update, self.draw)


  def update(self):
    if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
      pyxel.quit()

    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
      if self.player.y >= self.player.move_y:
        self.player.y -= self.player.move_y
    
    if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
      if self.player.y <= self._height - self.player.height - self.player.move_y:
        self.player.y += self.player.move_y
    
    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
      if self.player.x >= self.player.move_x:
        self.player.x -= self.player.move_x
    
    if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
      if self.player.x <= self._width - self.player.width - self.player.move_x:
        self.player.x += self.player.move_x

    # move missile
    for i in range(0, self.p_miss_max):
      if self.p_miss[i].x > self._width:
        self.p_miss_f[i] = False
      else:
        self.p_miss[i].x += self.p_miss[i].move_x

    # Z : fire
    if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
      nm = -1
      for i in range(0, self.p_miss_max):
        if not self.p_miss_f[i]:
          nm = i
          break
      if nm != -1:
        self.p_miss_f[nm] = True
        self.p_miss[nm].x = self.player.x + self.player.fire_x[self.player.res_num]
        self.p_miss[nm].y = self.player.y + self.player.fire_y[self.player.res_num]

    # player
    if self.turn % 5 == 0:
      self.player.res_num += 1
      if self.player.res_num == self.player.res_max:
        self.player.res_num = 0
    
    self.turn += 1


  def draw(self):
    pyxel.cls(12)

    pyxel.blt(
      self.player.x,
      self.player.y,
      self.player.res_page[self.player.res_num],
      self.player.res_u[self.player.res_num],
      self.player.res_v[self.player.res_num],
      self.player.res_w[self.player.res_num],
      self.player.res_h[self.player.res_num],
      self.player.res_col[self.player.res_num],
    )

    for i in range(0, self.p_miss_max):
      if self.p_miss_f[i]:
        pyxel.blt(
          self.p_miss[i].x,
          self.p_miss[i].y,
          self.p_miss[i].res_page[self.p_miss[i].res_num],
          self.p_miss[i].res_u[self.p_miss[i].res_num],
          self.p_miss[i].res_v[self.p_miss[i].res_num],
          self.p_miss[i].res_w[self.p_miss[i].res_num],
          self.p_miss[i].res_h[self.p_miss[i].res_num],
          self.p_miss[i].res_col[self.p_miss[i].res_num]
        )
    

App()

