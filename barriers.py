from turtle import Turtle


BARRIER1_X = -300
BARRIER2_X = 0
BARRIER3_X = 300
BARRIER_Y = -270


class Barriers:

  def __init__(self):
    self.all_barriers = [
      Barrier(BARRIER1_X, BARRIER_Y),
      Barrier(BARRIER2_X, BARRIER_Y),
      Barrier(BARRIER3_X, BARRIER_Y)
    ]

  def hit(self, barrier, damage):
    barrier.health -= damage
    if barrier.health == 4:
      barrier.shape("images/barrier2.gif")
    elif barrier.health == 2:
      barrier.shape("images/barrier3.gif")
    elif barrier.health == 0:
      self.explode(barrier)

  def explode(self, barrier):
    self.all_barriers.remove(barrier)
    barrier.reset()
    barrier.hideturtle()


class Barrier(Turtle):

  def __init__(self, x, y):
    super().__init__()
    self.shape("images/barrier1.gif")
    self.penup()
    self.health = 6

    self.goto(x, y)
    
