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
  hit  = 0

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
    self.playerres.add_burn(0, 48, 16, 16, 16, 0)
    self.playerres.add_burn(0, 64, 16, 16, 16, 0)

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
    self.enemylist[en].add_burn(0, 48, 0, 16, 16, 0)
    self.enemylist[en].add_burn(0, 64, 0, 16, 16, 0)
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
    self.enemylist[en].add_burn(0, 48, 0, 16, 16, 0)
    self.enemylist[en].add_burn(0, 64, 0, 16, 16, 0)
    self.enemylist[en].add_action(
      [ 0, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0, -3, -3, -3, -3, -3, -3, -3, -3]
    )

    # enemy
    for i in range(0, self.enemy_max):
      self.enemy_f.append(False)
      self.enemylist_n.append(0)
      self.enemy.append(Chara(0, 0, 0, 0))

    self.start()

    pyxel.init(self._width, self._height, title="test", fps=15)
    pyxel.load("assets/test.pyxres")
    pyxel.run(self.update, self.draw)


  def start(self):
    self.turn         = 0
    self.hit          = 0
    self.isAlive      = True
    self.player.turn  = 0
    self.player.res_n = 0

  def update(self):
    if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
      pyxel.quit()

    if self.isStop:
      return

    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
      if self.player.isAlive:
        if self.player.y >= self.player.move_y:
          self.player.y -= self.player.move_y
    
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
      if self.player.isAlive:
        if self.player.y <= self._height - self.player.height - self.player.move_y:
          self.player.y += self.player.move_y
    
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
      if self.player.isAlive:
        if self.player.x >= self.player.move_x:
          self.player.x -= self.player.move_x
    
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
      if self.player.isAlive:
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
      if self.player.isAlive:
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
    if self.player.turn % 5 == 0:
      if self.player.isAlive:
        self.player.res_n += 1
        if self.player.res_n == self.playerres.res_max:
          self.player.res_n = 0
      else:
        self.player.res_n += 1
        if self.player.res_n == self.playerres.burn_max:
          self.isStop = True 

    self.player.turn += 1
    
    # enemy
    if self.turn >= 20:
      if random.random() < 0.15:
        for i in range(0, self.enemy_max):
          if not self.enemy_f[i]:
            self.enemy_f[i]           = True
            self.enemylist_n[i]       = random.randrange(0, self.enemylist_max)
            self.enemy[i].x           = 280
            self.enemy[i].y           = random.randrange(50, self._height-50)
            self.enemy[i].turn        = 0
            self.enemy[i].res_n       = 0
            self.enemy[i].charamove_n = 0
            self.enemy[i].isAlive     = True
            break

    for i in range(0, self.enemy_max):
      if self.enemy_f[i] :
        if self.enemy[i].isAlive:
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

          if self.enemy[i].turn % 8 == 0:
            self.enemy[i].res_n += 1
            if self.enemy[i].res_n == self.enemylist[self.enemylist_n[i]].res_max :
              self.enemy[i].res_n = 0

        else:
          if self.enemy[i].turn % 8 == 0:
            self.enemy[i].res_n += 1
            if self.enemy[i].res_n == self.enemylist[self.enemylist_n[i]].burn_max :
              self.enemy_f[i] = False

        self.enemy[i].turn  += 1

    # hit check for player and enemy
    if self.player.isAlive:
      p_llx = self.player.x + self.playerres.hita_llx[self.player.res_n]
      p_lly = self.player.y + self.playerres.hita_lly[self.player.res_n]
      p_urx = self.player.x + self.playerres.hita_urx[self.player.res_n]
      p_ury = self.player.y + self.playerres.hita_ury[self.player.res_n]
      for i in range(0, self.enemy_max):
        if self.enemy_f[i] and self.enemy[i].isAlive:
          e_llx = self.enemy[i].x + self.enemylist[self.enemylist_n[i]].hita_llx[self.enemy[i].res_n]
          e_lly = self.enemy[i].y + self.enemylist[self.enemylist_n[i]].hita_lly[self.enemy[i].res_n]
          e_urx = self.enemy[i].x + self.enemylist[self.enemylist_n[i]].hita_urx[self.enemy[i].res_n]
          e_ury = self.enemy[i].y + self.enemylist[self.enemylist_n[i]].hita_ury[self.enemy[i].res_n]
          if max(p_llx, e_llx) < min(p_urx, e_urx) and max(p_lly, e_lly) < min(p_ury, e_ury):
            self.player.turn    = 1
            self.player.res_n   = 0
            self.player.isAlive = False
            #print("Hit")
            #print("  player %d %d %d %d" %(p_llx, p_lly, p_urx, p_ury))
            #print("  enemy  %d %d %d %d %d" %(i, e_llx, e_lly, e_urx, e_ury))
            #pyxel.rect(p_llx, p_lly, p_urx - p_llx, p_ury - p_lly + 1, 0)
            #pyxel.rect(e_llx, e_lly, e_urx - e_llx, e_ury - e_lly + 1, 0)
            #self.isStop = True
            break

    # hit check for player missiles and enemy
    for i in range(0, self.p_miss_max):
      if self.p_miss_f[i]:
        p_llx = self.p_miss[i].x + self.p_missres.hita_llx[0]
        p_lly = self.p_miss[i].y + self.p_missres.hita_lly[0]
        p_urx = self.p_miss[i].x + self.p_missres.hita_urx[0]
        p_ury = self.p_miss[i].y + self.p_missres.hita_ury[0]
      
        for j in range(0, self.enemy_max):
          if self.enemy_f[j] and self.enemy[j].isAlive:
            e_llx = self.enemy[j].x + self.enemylist[self.enemylist_n[j]].hita_llx[self.enemy[j].res_n]
            e_lly = self.enemy[j].y + self.enemylist[self.enemylist_n[j]].hita_lly[self.enemy[j].res_n]
            e_urx = self.enemy[j].x + self.enemylist[self.enemylist_n[j]].hita_urx[self.enemy[j].res_n]
            e_ury = self.enemy[j].y + self.enemylist[self.enemylist_n[j]].hita_ury[self.enemy[j].res_n]
            if max(p_llx, e_llx) < min(p_urx, e_urx) and max(p_lly, e_lly) < min(p_ury, e_ury):
              self.hit              += 1
              self.enemy[j].turn    = 1
              self.enemy[j].res_n   = 0
              self.enemy[j].isAlive = False
              self.p_miss_f[i]      = False
              #print("Hit")
              #print("  miss   %d %d %d %d" %(p_llx, p_lly, p_urx, p_ury))
              #print("  enemy  %d %d %d %d %d" %(i, e_llx, e_lly, e_urx, e_ury))
              #pyxel.rect(p_llx, p_lly, p_urx - p_llx, p_ury - p_lly + 1, 0)
              #pyxel.rect(e_llx, e_lly, e_urx - e_llx, e_ury - e_lly + 1, 0)
              break
              

    self.turn += 1


  def draw(self):
    if self.isStop:
      return

    pyxel.cls(12)

    pyxel.text(250, 4, "Turn " + str(self.turn).zfill(6), 7)
    pyxel.text(200, 4, "Hit " + str(self.hit).zfill(4), 7)

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
        if self.enemy[i].isAlive:
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
        else:
          #print("enemy %d list %d res %d" %(i, self.enemylist_n[i], self.enemy[i].res_n))
          #print("  %d" %(self.enemylist[self.enemylist_n[i]].burn_page[self.enemy[i].res_n]))
          pyxel.blt(
            self.enemy[i].x,
            self.enemy[i].y,
            self.enemylist[self.enemylist_n[i]].burn_page[self.enemy[i].res_n],
            self.enemylist[self.enemylist_n[i]].burn_u[self.enemy[i].res_n],
            self.enemylist[self.enemylist_n[i]].burn_v[self.enemy[i].res_n],
            self.enemylist[self.enemylist_n[i]].burn_w[self.enemy[i].res_n],
            self.enemylist[self.enemylist_n[i]].burn_h[self.enemy[i].res_n],
            self.enemylist[self.enemylist_n[i]].burn_col[self.enemy[i].res_n]
          )
    
    # Player
    if self.player.isAlive:
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
    else:
      #print("player turn %d res %d" %(self.player.turn, self.player.res_n))
      pyxel.blt(
        self.player.x,
        self.player.y,
        self.playerres.burn_page[self.player.res_n],
        self.playerres.burn_u[self.player.res_n],
        self.playerres.burn_v[self.player.res_n],
        self.playerres.burn_w[self.player.res_n],
        self.playerres.burn_h[self.player.res_n],
        self.playerres.burn_col[self.player.res_n],
      )


App()

