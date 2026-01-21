#
#

import random
import copy
import pyxel
from Chara import Chara
from CharaResource import CharaResource


class App:
  _miss_m = 10
  _cw     = 16
  _width  = 300
  _height = 200

  isStop     = False

  turn = 0

  player     = None
  playerres  = None
  p_miss_max = 6
  p_miss_f   = []
  p_miss     = []
  p_missres  = None

  enemy_max   = 10
  enemy_f     = []
  enemy       = []
  enemylist_n = []

  enemylist_max = 2
  enemylist     = []

  def __init__(self):

    # player settings
    self.player = Chara(40, 80, 8, 8)
    self.playerres = CharaResource()
    self.playerres.add_res(0, 0, 16, 16, 16, 0, 16, 7)
    self.playerres.add_res(0, 16, 16, 16, 16, 0, 16, 7)
    self.playerres.add_hita(0, 5, 13, 9)
    self.playerres.add_hita(0, 5, 13, 9)

    self.p_missres = CharaResource()
    self.p_missres.add_res(0, 38, 23, 4, 2, 12)
    self.p_missres.add_hita(6, 7, 9, 8)

    # player missile settings
    for i in range(0, self.p_miss_max):
      self.p_miss_f.append(False)
      self.p_miss.append(Chara(0, 0, 10, 0))

    # enemy list
    en = 0
    self.enemylist.append(CharaResource())
    self.enemylist[en].add_res(0, 0, 0, 16, 16, 0, 0, 7)
    self.enemylist[en].add_res(0, 16, 0, 16, 16, 0, 0, 7)
    self.enemylist[en].add_hita(0, 0, 15, 15)
    self.enemylist[en].add_hita(0, 0, 15, 15)
    self.enemylist[en].add_action(
      [ 0, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  3,  3,  3,  3,  3,  3,  3]
    )

    en += 1
    self.enemylist.append(CharaResource())
    self.enemylist[en].add_res(0, 0, 0, 16, 16, 0, 0, 7)
    self.enemylist[en].add_res(0, 16, 0, 16, 16, 0, 0, 7)
    self.enemylist[en].add_hita(0, 0, 15, 15)
    self.enemylist[en].add_hita(0, 0, 15, 15)
    self.enemylist[en].add_action(
      [ 0, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0, -3, -3, -3, -3, -3, -3, -3, -3]
    )

    # enemy
    for i in range(0, self.enemy_max):
      self.enemy_f.append(False)
      self.enemylist_n.append(0)
      self.enemy.append(Chara(0, 0, 0, 0))

    pyxel.init(self._width, self._height, title="test", fps=15)
    pyxel.load("assets/test.pyxres")
    pyxel.run(self.update, self.draw)


  def update(self):
    if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
      pyxel.quit()

    if self.isStop:
      return

    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
      if self.player.y >= self.player.move_y:
        self.player.y -= self.player.move_y
    
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
      if self.player.y <= self._height - self.player.height - self.player.move_y:
        self.player.y += self.player.move_y
    
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
      if self.player.x >= self.player.move_x:
        self.player.x -= self.player.move_x
    
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
      if self.player.x <= self._width - self.player.width - self.player.move_x:
        self.player.x += self.player.move_x

    # move missile
    for i in range(0, self.p_miss_max):
      if self.p_miss_f[i] :
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
        self.p_miss[nm].x = self.player.x + self.playerres.fire_x[self.player.res_n]
        self.p_miss[nm].y = self.player.y + self.playerres.fire_y[self.player.res_n]

    # player
    if self.turn % 5 == 0:
      self.player.res_n += 1
      if self.player.res_n == self.playerres.res_max:
        self.player.res_n = 0
    
    # enemy
    if self.turn >= 20:
      if random.random() < 0.15:
        for i in range(0, self.enemy_max):
          if not self.enemy_f[i]:
            self.enemy_f[i]           = True
            self.enemylist_n[i]       = random.randrange(0, self.enemylist_max)
            self.enemy[i].x           = 280
            self.enemy[i].y           = random.uniform(5, self._height-100)
            self.enemy[i].turn        = 0
            self.enemy[i].res_n       = 0
            self.enemy[i].charamove_n = 0
            break

    for i in range(0, self.enemy_max):
      if self.enemy_f[i] :
        self.enemy[i].x += self.enemylist[self.enemylist_n[i]].charamove.x[self.enemy[i].charamove_n]
        self.enemy[i].y += self.enemylist[self.enemylist_n[i]].charamove.y[self.enemy[i].charamove_n]
        #print("enemy %d turn %d move n %d x %d y %d" %(i, self.enemy[i].turn, self.enemy[i].charamove_n, self.enemylist[self.enemylist_n[i]].charamove.x[self.enemy[i].charamove_n], self.enemylist[self.enemylist_n[i]].charamove.y[self.enemy[i].charamove_n]))

        if self.enemy[i].x < 0:
          self.enemy_f[i] = False
        if self.enemy[i].y < 0:
          self.enemy_f[i] = False
        if self.enemy[i].x > self._width:
          self.enemy_f[i] = False
        if self.enemy[i].y > self._height:
          self.enemy_f[i] = False

        self.enemy[i].charamove_n += 1
        if self.enemy[i].charamove_n == self.enemylist[self.enemylist_n[i]].charamove_num:
          self.enemy[i].charamove_n = 0

        if self.enemy[i].turn % 5 == 0:
          self.enemy[i].res_n += 1
          if self.enemy[i].res_n == self.enemylist[self.enemylist_n[i]].res_max :
            self.enemy[i].res_n = 0

        self.enemy[i].turn  += 1

    # hit player and enemy
    p_llx = self.player.x + self.playerres.hita_llx[self.player.res_n]
    p_lly = self.player.y + self.playerres.hita_lly[self.player.res_n]
    p_urx = self.player.x + self.playerres.hita_urx[self.player.res_n]
    p_ury = self.player.y + self.playerres.hita_ury[self.player.res_n]
    for i in range(0, self.enemy_max):
      if self.enemy_f[i] :
        e_llx = self.enemy[i].x + self.enemylist[self.enemylist_n[i]].hita_llx[self.player.res_n]
        e_lly = self.enemy[i].y + self.enemylist[self.enemylist_n[i]].hita_lly[self.player.res_n]
        e_urx = self.enemy[i].x + self.enemylist[self.enemylist_n[i]].hita_urx[self.player.res_n]
        e_ury = self.enemy[i].y + self.enemylist[self.enemylist_n[i]].hita_ury[self.player.res_n]
        if max(p_llx, e_llx) < min(p_urx, e_urx) and max(p_lly, e_lly) < min(p_ury, e_ury):
          print("Hit")
          print("  player %d %d %d %d" %(p_llx, p_lly, p_urx, p_ury))
          print("  enemy  %d %d %d %d %d" %(i, e_llx, e_lly, e_urx, e_ury))
          #pyxel.rect(p_llx, p_lly, p_urx - p_llx, p_ury - p_lly + 1, 0)
          #pyxel.rect(e_llx, e_lly, e_urx - e_llx, e_ury - e_lly + 1, 0)
          self.isStop = True
          break

    self.turn += 1


  def draw(self):
    if self.isStop:
      return

    pyxel.cls(12)

    pyxel.text(250, 4, "Turn " + str(self.turn).zfill(6), 7)

    # Player
    pyxel.blt(
      self.player.x,
      self.player.y,
      self.playerres.res_page[self.player.res_n],
      self.playerres.res_u[self.player.res_n],
      self.playerres.res_v[self.player.res_n],
      self.playerres.res_w[self.player.res_n],
      self.playerres.res_h[self.player.res_n],
      self.playerres.res_col[self.player.res_n],
    )

    # Player missile
    for i in range(0, self.p_miss_max):
      if self.p_miss_f[i]:
        pyxel.blt(
          self.p_miss[i].x,
          self.p_miss[i].y,
          self.p_missres.res_page[self.p_miss[i].res_n],
          self.p_missres.res_u[self.p_miss[i].res_n],
          self.p_missres.res_v[self.p_miss[i].res_n],
          self.p_missres.res_w[self.p_miss[i].res_n],
          self.p_missres.res_h[self.p_miss[i].res_n],
          self.p_missres.res_col[self.p_miss[i].res_n]
        )
    
    # Enemy
    for i in range(0, self.enemy_max):
      if self.enemy_f[i]:
        pyxel.blt(
          self.enemy[i].x,
          self.enemy[i].y,
          self.enemylist[self.enemylist_n[i]].res_page[self.enemy[i].res_n],
          self.enemylist[self.enemylist_n[i]].res_u[self.enemy[i].res_n],
          self.enemylist[self.enemylist_n[i]].res_v[self.enemy[i].res_n],
          self.enemylist[self.enemylist_n[i]].res_w[self.enemy[i].res_n],
          self.enemylist[self.enemylist_n[i]].res_h[self.enemy[i].res_n],
          self.enemylist[self.enemylist_n[i]].res_col[self.enemy[i].res_n]
        )
    

App()

