#
# horizontal scroll shooting
#
# library
#   pyxel

import random
import pyxel
from Chara import Chara
from CharaResource import CharaResource


class App:
  _miss_m = 10		# number of missiles
  _width  = 300		# screen width
  _height = 200		# screen height

  #isStop     = True	# Game stop
  gamemode   = 0	# Game mode (0=menu, 1=on play, 2=game over)

  turn = 0		# number of turn (frame)
  hit  = 0		# number of hit

  player     = None	# player character
  playerres  = None	# player character resource
  p_miss_max = 6	# number of player missiles
  p_miss_f   = []	# flags of missiles
  p_miss     = []	# missiles character
  p_missres  = None	# missiles character resource

  enemy_max   = 10	# number of enemies
  enemy_f     = []	# flags of enemy
  enemy       = []	# enemy character
  enemylist_n = []	# resource number of enemy list

  enemymiss_max = 30	# number of enemy's missiles
  enemymiss_f   = []	# flags of enemy's missiles
  enemymiss     = []	# enemies charater
  enemymissres  = None	# enemy missile resource

  enemylist_max = 2	# number of enemy resource
  enemylist     = []	# enemy resources


  def __init__(self):

    pyxel.init(self._width, self._height, title="test", fps=15)
    pyxel.load("assets/test.pyxres")

    # player settings
    self.player = Chara(40, 80, 6, 6)
    self.playerres = CharaResource()
    self.playerres.add_res(0, 0, 16, 16, 16, 0, 16, 7)
    self.playerres.add_res(0, 16, 16, 16, 16, 0, 16, 7)
    self.playerres.add_hita(0, 5, 13, 9)
    self.playerres.add_hita(0, 5, 13, 9)
    self.playerres.add_burn(0, 48, 16, 16, 16, 0)
    self.playerres.add_burn(0, 64, 16, 16, 16, 0)

    self.p_missres = CharaResource()
    self.p_missres.add_res(0, 38, 23, 4, 2, 12)
    self.p_missres.add_hita(0, 0, 4, 2)

    # player missile settings
    for i in range(0, self.p_miss_max):
      self.p_miss_f.append(False)
      self.p_miss.append(Chara(0, 0, 10, 0))

    # enemy list
    en = 0
    self.enemylist.append(CharaResource())
    self.enemylist[en].add_res(0, 0, 0, 16, 16, 0, 7, 7)
    self.enemylist[en].add_res(0, 16, 0, 16, 16, 0, 7, 7)
    self.enemylist[en].add_hita(0, 0, 15, 15)
    self.enemylist[en].add_hita(0, 0, 15, 15)
    self.enemylist[en].add_burn(0, 48, 0, 16, 16, 0)
    self.enemylist[en].add_burn(0, 64, 0, 16, 16, 0)
    self.enemylist[en].add_action(
      [ 0, -3, -3, -3, -3, -3, -3,  0,  0,  0,  0, -3, -3, -3, -3, -3, -3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  3,  3,  3,  3,  3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0]
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
      [ 0, -3, -3, -3, -3, -3, -3,  0,  0,  0,  0, -3, -3, -3, -3, -3, -3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -3, -3, -3, -3, -3, -3],
      [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0]
    )

    # enemy
    for i in range(0, self.enemy_max):
      self.enemy_f.append(False)
      self.enemylist_n.append(0)
      self.enemy.append(Chara(0, 0, 0, 0))

    # enemy missiles
    self.enemymissres = CharaResource()
    self.enemymissres.add_res(0, 39, 7, 2, 2, 12)
    self.enemymissres.add_hita(0, 0, 1, 1)
    for i in range(0, self.enemymiss_max):
      self.enemymiss_f.append(False)
      self.enemymiss.append(Chara(0, 0, 3, 3))


    #self.start()

    pyxel.run(self.update, self.draw)


  def start(self):
    self.gamemode       = 1
    self.turn           = 0
    self.hit            = 0
    self.player.x       = 40
    self.player.y       = 80
    self.player.turn    = 0
    self.player.res_n   = 0
    self.player.isAlive = True

    for i in range(0, self.p_miss_max):
      self.p_miss_f[i] = False

    for i in range(0, self.enemy_max):
      self.enemy_f[i] = False

    for i in range(0, self.enemymiss_max):
      self.enemymiss_f[i] = False

    pyxel.play(0, 2, loop=True)


  def update(self):
    # "Q" for quit
    if pyxel.btnp(pyxel.KEY_Q):
      pyxel.quit()

    # Gate stop
    if self.gamemode == 0:

      if self.player.turn % 5 == 0:
        self.player.res_n += 1
        if self.player.res_n == self.playerres.res_max:
          self.player.res_n = 0
      
      self.player.turn += 1

      if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
        self.start()
        self.gamemode = 1
      return

    # Game over
    if self.gamemode == 2:
      if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
        self.gamemode = 0
      return


    # on play

    # "Up" key
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
      if self.player.isAlive:
        if self.player.y >= self.player.move_y:
          self.player.y -= self.player.move_y
    
    # "Down" key
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
      if self.player.isAlive:
        if self.player.y <= self._height - self.player.height - self.player.move_y:
          self.player.y += self.player.move_y
    
    # "Left" key
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
      if self.player.isAlive:
        if self.player.x >= self.player.move_x:
          self.player.x -= self.player.move_x
    
    # "Right" key
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
      if self.player.isAlive:
        if self.player.x <= self._width - self.player.width - self.player.move_x:
          self.player.x += self.player.move_x

    # move missiles
    for i in range(0, self.p_miss_max):
      if self.p_miss_f[i] :
        if self.p_miss[i].x > self._width:
          self.p_miss_f[i] = False
        else:
          self.p_miss[i].x += self.p_miss[i].move_x
          self.p_miss[i].y += self.p_miss[i].move_y

    # "Z" key for fire
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
          pyxel.play(1, 0)

    # change player resource
    if self.player.turn % 5 == 0:
      if self.player.isAlive:
        self.player.res_n += 1
        if self.player.res_n == self.playerres.res_max:
          self.player.res_n = 0
      else:
        self.player.res_n += 1
        if self.player.res_n == self.playerres.burn_max:
          self.gamemode     = 2
          self.player.turn  = 0
          self.player.res_n = 0
          return

    self.player.turn += 1
    
    # move enemy missiles
    for i in range(0, self.enemymiss_max):
      if self.enemymiss_f[i]:
        self.enemymiss[i].x += self.enemymiss[i].move_x
        self.enemymiss[i].y += self.enemymiss[i].move_y

        if self.enemymiss[i].x < 0:
          self.enemymiss_f[i] = False
        if self.enemymiss[i].y < 0:
          self.enemymiss_f[i] = False
        if self.enemymiss[i].x > self._width:
          self.enemymiss_f[i] = False
        if self.enemymiss[i].y > self._height:
          self.enemymiss_f[i] = False

    # add enemies
    if self.turn >= 20:
      if random.random() < 0.15:
        for i in range(0, self.enemy_max):
          if not self.enemy_f[i]:
            self.enemy_f[i]           = True
            self.enemylist_n[i]       = random.randrange(0, self.enemylist_max)
            self.enemy[i].x           = self._width
            self.enemy[i].y           = random.randrange(50, self._height-50)
            self.enemy[i].turn        = 0
            self.enemy[i].res_n       = 0
            self.enemy[i].charamove_n = 0
            self.enemy[i].isAlive     = True
            break

    # move enemies
    for i in range(0, self.enemy_max):
      if self.enemy_f[i] :
        if self.enemy[i].isAlive:
          self.enemy[i].x += self.enemylist[self.enemylist_n[i]].charamove.x[self.enemy[i].charamove_n]
          self.enemy[i].y += self.enemylist[self.enemylist_n[i]].charamove.y[self.enemy[i].charamove_n]

          # fire
          if self.enemylist[self.enemylist_n[i]].charamove.attack[self.enemy[i].charamove_n] == 1:
            nm = -1
            for j in range(0, self.enemymiss_max):
              if not self.enemymiss_f[j]:
                nm = j
                break
            if nm != -1:
              self.enemymiss_f[nm] = True
              self.enemymiss[nm].x = self.enemy[i].x + self.enemylist[self.enemylist_n[i]].fire_x[self.enemy[i].res_n]
              self.enemymiss[nm].y = self.enemy[i].y + self.enemylist[self.enemylist_n[i]].fire_y[self.enemy[i].res_n]
              dx = self.player.x + self.player.width  / 2 - self.enemymiss[nm].x
              dy = self.player.y + self.player.height / 2 - self.enemymiss[nm].y
              if abs(dx) > abs(dy):
                self.enemymiss[nm].move_x = dx / abs(dx) * 3
                self.enemymiss[nm].move_y = dy / abs(dx) * 3
              else:
                self.enemymiss[nm].move_x = dx / abs(dy) * 3
                self.enemymiss[nm].move_y = dy / abs(dy) * 3
              self.enemymiss[nm].turn   = 0
  
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

        # when enemies is dead
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
            pyxel.stop(0)
            pyxel.play(3, 3)
            #pyxel.rect(p_llx, p_lly, p_urx - p_llx, p_ury - p_lly + 1, 0)
            #pyxel.rect(e_llx, e_lly, e_urx - e_llx, e_ury - e_lly + 1, 0)
            break

    # hit check for player and enemy missiles
    if self.player.isAlive:
      for i in range(0, self.enemymiss_max):
        if self.enemymiss_f[i]:
          e_llx = self.enemymiss[i].x + self.enemymissres.hita_llx[0]
          e_lly = self.enemymiss[i].y + self.enemymissres.hita_lly[0]
          e_urx = self.enemymiss[i].x + self.enemymissres.hita_urx[0]
          e_ury = self.enemymiss[i].y + self.enemymissres.hita_ury[0]
          if max(p_llx, e_llx) <= min(p_urx, e_urx) and max(p_lly, e_lly) <= min(p_ury, e_ury):
            self.player.turn    = 1
            self.player.res_n   = 0
            self.player.isAlive = False
            pyxel.stop(0)
            pyxel.play(3, 3)
            #pyxel.rect(p_llx, p_lly, p_urx - p_llx, p_ury - p_lly + 1, 0)
            #pyxel.rect(e_llx, e_lly, e_urx - e_llx, e_ury - e_lly + 1, 0)
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
              pyxel.play(2, 1)
              #pyxel.rect(p_llx, p_lly, p_urx - p_llx, p_ury - p_lly + 1, 0)
              #pyxel.rect(e_llx, e_lly, e_urx - e_llx, e_ury - e_lly + 1, 0)
              break
              

    self.turn += 1


  def draw(self):
    pyxel.cls(12)

    if self.gamemode == 0:	# menu
      pyxel.blt(
        self._width / 2 - self.player.width,
        self._height / 3 - self.player.height,
        self.playerres.res_page[self.player.res_n],
        self.playerres.res_u[self.player.res_n],
        self.playerres.res_v[self.player.res_n],
        self.playerres.res_w[self.player.res_n],
        self.playerres.res_h[self.player.res_n],
        self.playerres.res_col[self.player.res_n],
      )
      pyxel.text(120, 110, "Cursor : Move", 7)
      pyxel.text(120, 120, "  z    : shoot", 7)
      pyxel.text(110, 150, "Push \"z\" key to start", 7)
      return

    #if self.gamemode == 2:	# game over
    #  return


    # on play

    #pyxel.text(0, 4, "Turn " + str(self.turn).zfill(6), 7)
    pyxel.text(250, 4, "Hit " + str(self.hit).zfill(4), 7)

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
        #p_llx = self.p_miss[i].x + self.p_missres.hita_llx[0]
        #p_lly = self.p_miss[i].y + self.p_missres.hita_lly[0]
        #p_urx = self.p_miss[i].x + self.p_missres.hita_urx[0]
        #p_ury = self.p_miss[i].y + self.p_missres.hita_ury[0]
        #pyxel.rect(p_llx, p_lly, p_urx - p_llx + 1, p_ury - p_lly + 1, 0)
    
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
    
    # Enemy missles
    for i in range(0, self.enemymiss_max):
      if self.enemymiss_f[i]:
        pyxel.blt(
          self.enemymiss[i].x,
          self.enemymiss[i].y,
          self.enemymissres.res_page[0],
          self.enemymissres.res_u[0],
          self.enemymissres.res_v[0],
          self.enemymissres.res_w[0],
          self.enemymissres.res_h[0],
          self.enemymissres.res_col[0]
        )
        #e_llx = self.enemymiss[i].x + self.enemymissres.hita_llx[0]
        #e_lly = self.enemymiss[i].y + self.enemymissres.hita_lly[0]
        #e_urx = self.enemymiss[i].x + self.enemymissres.hita_urx[0]
        #e_ury = self.enemymiss[i].y + self.enemymissres.hita_ury[0]
        #pyxel.rect(e_llx, e_lly, e_urx - e_llx + 1, e_ury - e_lly + 1, 0)

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

    if self.gamemode == 2:
      pyxel.text(120, 100, str(self.hit) + " hits", 7)
      pyxel.text(120, 150, "Push \"z\" key", 7)

App()

