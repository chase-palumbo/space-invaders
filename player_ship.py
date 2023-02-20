from turtle import Turtle


SHIP_Y = -400
SHIP_STARTING_X = 0
BULLET_STARTING_Y = SHIP_Y + 40
MOVE_DISTANCE = 15
BULLET_MOVE_DISTANCE = 25

LEFT_EDGE = -460
RIGHT_EDGE = 445

class PlayerShip(Turtle):

  def __init__(self):
    super().__init__()

    self.game_on = False

    self.cur_x = SHIP_STARTING_X
    self.cur_y = SHIP_Y
    self.inactive_bullets = [Bullet(), Bullet(), Bullet(), Bullet()]
    self.active_bullets = []

    self.penup()
    self.shape("images/spaceship.gif")
    self.move_ship()

  def left(self):
    if self.cur_x > LEFT_EDGE:
      self.cur_x -= MOVE_DISTANCE
      self.move_ship()

  def right(self):
    if self.cur_x < RIGHT_EDGE:
      self.cur_x += MOVE_DISTANCE
      self.move_ship()

  def move_ship(self):
    self.goto(self.cur_x, self.cur_y)

  def shoot(self):
    if self.inactive_bullets != []:
      new_bullet = self.inactive_bullets.pop()
      new_bullet.active = True
      new_bullet.set_starting_pos(self.cur_x)
      self.active_bullets.append(new_bullet)

  def recycle_bullet(self, bullet):
    self.active_bullets.remove(bullet)
    bullet.collision()
    self.inactive_bullets.append(bullet)

  def hit(self):
    self.shape("images/explosion.gif")

  def reset_pos(self):
    self.cur_x = SHIP_STARTING_X
    self.cur_y = SHIP_Y
    self.move_ship()

      
class Bullet(Turtle):

  def __init__(self):
    super().__init__("square")
    self.penup()
    self.color("white")
    self.shapesize(stretch_len=0.2)
    self.hideturtle()

    self.active = False
  
  def set_starting_pos(self, ship_x):
    self.cur_y = BULLET_STARTING_Y
    self.cur_x = ship_x
    self.goto(self.cur_x, self.cur_y)
    self.showturtle()

  def move(self):
    self.cur_y += BULLET_MOVE_DISTANCE
    self.goto(self.cur_x, self.cur_y)

  def collision(self):
    self.active = False
    self.hideturtle()

  
      
      



  















