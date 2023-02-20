from turtle import Turtle
import random


ALIEN_BULLET_MOVE = -20
ALIEN_X_MOVE_DIS = 2
ALIEN_Y_MOVE_DIS = -30

SUPER_ALIEN_Y = 370
SUPER_MOVE_DISTANCE = 10


### ALIEN TYPES ###
class Alien(Turtle):

  def __init__(self, x, y):
    super().__init__()
    self.penup()
    self.cur_x = x
    self.cur_y = y
    self.move_dis = ALIEN_X_MOVE_DIS
    self.y_move_dis = ALIEN_Y_MOVE_DIS

    self.goto(x, y)

  def move(self, direction):
    if direction == "right":
      self.cur_x += self.move_dis
    else:
      self.cur_x -= self.move_dis
      
    self.goto(self.cur_x, self.cur_y)

  def move_up(self):
    self.cur_y += self.y_move_dis
    self.goto(self.cur_x, self.cur_y) 

  def shoot(self):
      bullet_x = self.cur_x
      bullet_y = self.cur_y - 40
      self.bullet.set_starting_pos(bullet_x, bullet_y)

  def increase_speed(self):
    self.move_dis += 1


class PurpleAlien(Alien):

  def __init__(self, x, y):
    super().__init__(x, y)
    self.shape("images/purple-alien.gif")

    self.points = 10
    self.type = "purple"
    self.bullet = SmallBullet()


class GreenAlien(Alien):

  def __init__(self, x, y):
    super().__init__(x, y)
    self.shape("images/green-alien.gif")

    self.points = 20
    self.type = "green"
    self.bullet = SmallBullet()


class RedAlien(Alien):

  def __init__(self, x, y):
    super().__init__(x, y)
    self.shape("images/red-alien.gif")

    self.points = 30
    self.type = "red"
    self.bullet = BigBullet()


class SuperAlien(Turtle):

  def __init__(self):
    super().__init__()
    self.penup()
    self.shape("images/super-alien.gif")
    self.hideturtle()

    self.cur_y = SUPER_ALIEN_Y
    self.points = 100
    self.type = "super"
    self.bullet = SuperBullet()
    self.active = False

  def spawn(self):
    self.active = True
    self.direction = random.choice(["left", "right"])

    if self.direction == "right":
      self.x_shoot_cor = random.choice([-300, -250, -100, 50, 200])
      self.cur_x = -550
      self.move_dis = SUPER_MOVE_DISTANCE
    else:
      self.x_shoot_cor = random.choice([-200, -50, 100, 250, 300])
      self.cur_x = 550
      self.move_dis = -SUPER_MOVE_DISTANCE
    
    self.goto(self.cur_x, self.cur_y)
    self.showturtle()

  def move(self):
    self.cur_x += self.move_dis
    self.goto(self.cur_x, self.cur_y)

    if not self.bullet.bullet_used:
      if (self.direction == "right" and self.cur_x >= self.x_shoot_cor) or (self.direction == "left" and self.cur_x <= self.x_shoot_cor):
        # shoot bullet
        self.shoot()

    # move bullet with ship
    if self.bullet.active:
      self.bullet.move(self.cur_x)

    if self.cur_x > 600 or self.cur_x < -600:
      self.despawn()

  def shoot(self):
    bullet_x = self.cur_x
    bullet_y = self.cur_y - 60
    self.bullet.activate(bullet_x, bullet_y)

  def despawn(self):
    self.active = False
    self.hideturtle()
    self.shape("images/super-alien.gif")
    self.bullet.bullet_used = False

    if self.bullet.active:
      self.bullet.deactivate()


### BULLET TYPES ###
class Bullet(Turtle):

  def __init__(self):
    super().__init__()
    self.penup()
    self.hideturtle()

    self.move_speed = ALIEN_BULLET_MOVE
    self.active = False

  def set_starting_pos(self, ship_x, ship_y):
    self.active = True
    self.cur_x = ship_x
    self.cur_y = ship_y
    self.goto(self.cur_x, self.cur_y)
    self.showturtle()

  def move(self):
    self.cur_y += self.move_speed
    self.goto(self.cur_x, self.cur_y)

  def collision(self):
    self.active = False
    self.hideturtle()


class SmallBullet(Bullet):

  def __init__(self):
    super().__init__()
    self.shape("square")
    self.color("red")
    self.shapesize(stretch_len=0.2)
    
    self.dmg = 1


class BigBullet(Bullet):

  def __init__(self):
    super().__init__()
    self.shape("circle")
    self.color("#ff0000")
    self.shapesize(stretch_len=1.5, stretch_wid=1.5)

    self.dmg = 2
    self.flash_toggle = False

  def flash(self):
    self.flash_toggle = not self.flash_toggle
    if self.flash_toggle:
      self.color("#ff9999")
    else:
      self.color("#ff0000")

  def move(self):
    super().move()
    self.flash()


class SuperBullet(Turtle):

  def __init__(self):
    super().__init__("square")
    self.penup()
    self.color("white")
    self.hideturtle()

    self.active = False
    self.bullet_used = False
    self.flash_toggle = False
    self.move_frame = 0

    self.length = 2
    self.max_length = 38
    self.y_cor_move = -20
    self.collision_point = (0, 0)

  def activate(self, x, y):
    self.shapesize(stretch_len=0.2, stretch_wid=self.length)
    self.active = True
    self.bullet_used = True
    self.showturtle()
    self.cur_x = x
    self.cur_y = y
    self.goto(x, y)
    
  def move(self, x):
    if self.length < self.max_length:
      self.length += 2
      self.shapesize(stretch_len=0.2, stretch_wid=self.length)
      self.cur_y += self.y_cor_move

    self.move_frame += 1
    # 2 seconds
    if self.move_frame == 40:
      self.deactivate()
      return
    
    self.cur_x = x
    self.goto(self.cur_x, self.cur_y)

    x_collision = self.cur_x - 2
    y_collision = self.cur_y - (self.length * 20) / 2
    self.collision_point = (x_collision, y_collision)

    self.flash()

  def flash(self):
    self.flash_toggle = not self.flash_toggle
    if self.flash_toggle:
      self.color("#0000f0")
    else:
      self.color("#00b4f0")

  def deactivate(self):
    self.active = False
    self.collision_point = (0, 0)
    self.length = 2
    self.move_frame = 0

    self.goto(0, 0)
    self.hideturtle()













