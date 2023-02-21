from turtle import Turtle

SCOREBOARD_X = -300
SCOREBOARD_Y = 420

HIGHSCORE_X = -50
HIGHSCORE_Y = 425

LIVES_X = 150
LIVES_Y = 420
LIVES_IMG_START_X = 270
LIVES_IMG_Y = 435

FONT = ("System", 30, "bold")


class Scoreboard:

  def __init__(self):
    self.score_text = Turtle()
    self.score_text.hideturtle()
    self.score_text.penup()
    self.score_text.color("white")
    self.score_text.goto(SCOREBOARD_X, SCOREBOARD_Y)

    self.high_score_text = Turtle()
    self.high_score_text.hideturtle()
    self.high_score_text.penup()
    self.high_score_text.color("white")
    self.high_score_text.goto(HIGHSCORE_X, HIGHSCORE_Y)

    self.lives_text = Turtle()
    self.lives_text.hideturtle()
    self.lives_text.penup()
    self.lives_text.color("white")
    self.lives_text.goto(LIVES_X, LIVES_Y)

    self.score = 0
    self.lives = 3
    self.life_turtles = [
      LifeImg(LIVES_IMG_START_X, LIVES_IMG_Y), 
      LifeImg(LIVES_IMG_START_X + 80, LIVES_IMG_Y), 
      LifeImg(LIVES_IMG_START_X + 160, LIVES_IMG_Y)
    ]

    self.write_score()
    self.write_lives()
    self.read_high_score()

  def write_score(self):
    self.score_text.clear()
    self.score_text.write(
      f"Score    {self.score}", 
      align="center", 
      font=FONT
    )

  def update_score(self, points):
    self.score += points
    self.write_score()

  def read_high_score(self):
    try:
      with open("high_score.txt", "r") as file:
        high_score = file.read()
    except FileNotFoundError:
      high_score = "0"
    self.high_score = int(high_score.strip())
    self.update_high_score_text()

  def write_high_score(self):
    with open("high_score.txt", "w") as file:
      file.write(str(self.score))
    self.high_score = self.score
    self.update_high_score_text()
    
  def update_high_score_text(self):
    self.high_score_text.clear()
    self.high_score_text.write(
      f"Highscore  {self.high_score}",
      align="center",
      font=("System", 20, "bold")
    )

  def write_lives(self):
    self.lives_text.clear()
    self.lives_text.write(
      f"Lives",
      align="center",
      font=FONT
    )

  def update_lives(self):
    self.lives -= 1
    turtle = self.life_turtles.pop()
    turtle.reset()
    turtle.hideturtle()

  def game_start(self):
    self.start_text = Turtle()
    self.start_text.hideturtle()
    self.start_text.penup()
    self.start_text.color("white")
    self.write_start()
    
  def write_start(self):
    self.start_text.write(
      "PLAYER 1 START",
      align="center",
      font=FONT
    )

  def remove_start_text(self):
    self.start_text.reset()
    self.start_text.hideturtle()

  def game_won(self):
    self.winner_text = Turtle()
    self.winner_text.penup()
    self.winner_text.hideturtle()
    self.winner_text.color("white")
    self.winner_text.write(
      "YOU WIN!",
      align="center",
      font=FONT
    )

    if self.score > self.high_score:
      self.write_high_score()

  def game_over(self, message):
    self.game_over_text = Turtle()
    self.game_over_text.penup()
    self.game_over_text.hideturtle()
    self.game_over_text.color("white")
    self.game_over_text.write(
      f"{message}\nGAME OVER",
      align="center",
      font=FONT
    )
    

class LifeImg(Turtle):

  def __init__(self, x, y):
    super().__init__()
    self.shape("images/lives.gif")
    self.penup()

    self.goto(x, y)