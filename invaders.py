import random
from aliens import PurpleAlien, GreenAlien, RedAlien, SuperAlien

ALIEN_START_X = -320
RED_ALIEN_START_X = -322
PURPLE_START_Y = 50
GREEN_START_Y = 170
RED_START_Y = 300

X_SPREAD = 75
Y_SPREAD = 60
RIGHT_EDGE = 460
LEFT_EDGE = -460
BREACH_Y = -230

ALIEN_BULLET_MOVE = -20


class Invaders:

  def __init__(self):
    self.all_enemies = []
    self.direction = "right"
    self.left_edge_hit = False
    self.right_edge_hit = False
    self.active_bullets = []
    self.hit_aliens = []
    self.breached = False

    self.create_alien_rows()
    
  def create_alien_rows(self):
    self.starting_x = ALIEN_START_X
    self.red_starting_x = RED_ALIEN_START_X
    self.purple_y = PURPLE_START_Y
    self.green_y = GREEN_START_Y
    self.red_y = RED_START_Y
    self.purple_aliens = []
    self.green_aliens = []
    self.red_aliens = []
    self.super_alien = SuperAlien()

    for _ in range(10):
      self.purple_aliens.append(PurpleAlien(self.starting_x, self.purple_y))
      self.purple_aliens.append(
        PurpleAlien(self.starting_x, self.purple_y + Y_SPREAD)
      )

      self.green_aliens.append(GreenAlien(self.starting_x, self.green_y))
      self.green_aliens.append(
        GreenAlien(self.starting_x, self.green_y + Y_SPREAD)
      )

      self.red_aliens.append(RedAlien(self.red_starting_x, self.red_y))

      self.starting_x += X_SPREAD
      self.red_starting_x += X_SPREAD

    self.all_enemies += self.purple_aliens + self.green_aliens + self.red_aliens

    ### TESTING ###
    # self.all_enemies += self.red_aliens
    
  def alien_hit(self, alien):
    if alien.type == "super":
      alien.active = False
      alien.bullet.deactivate()
    else:
      self.all_enemies.remove(alien)

      if len(self.all_enemies) == 30 or len(self.all_enemies) == 20 or len(self.all_enemies) == 10:
         for enemy in self.all_enemies:
          enemy.increase_speed()

    alien.shape("images/explosion.gif")
    alien.hit_frame = 0
    self.hit_aliens.append(alien)

  def explosions_handler(self):
    self.aliens_to_remove = []
    for alien in self.hit_aliens:
      alien.hit_frame += 1

      if alien.hit_frame == 4:
        self.aliens_to_remove.append(alien)
        if alien.type == "super":
          alien.despawn()
        else:
          alien.reset()
          alien.hideturtle()

    for alien in self.aliens_to_remove:
      self.hit_aliens.remove(alien)

  def move_aliens(self):
    if self.super_alien.active:
      self.super_alien.move()

    if self.hit_aliens != []:
      self.explosions_handler()

    if self.right_edge_hit:
      self.direction = "left"
      self.move_aliens_up()
      return
    if self.left_edge_hit:
      self.direction = "right"
      self.move_aliens_up()
      return
    
    for alien in self.all_enemies:
      alien.move(self.direction)

      if alien.cur_x >= RIGHT_EDGE:
        self.right_edge_hit = True
      elif alien.cur_x <= LEFT_EDGE:
        self.left_edge_hit = True

  def move_aliens_up(self):
    for alien in self.all_enemies:
      alien.move_up()

      if alien.cur_y <= BREACH_Y:
        self.breached = True

    self.right_edge_hit = False
    self.left_edge_hit = False

  def alien_attack(self):
    if self.all_enemies == [] or len(self.active_bullets) >= 5:
      return

    # 1/10 chance to shoot every frame
    rand_int = random.randint(1, 10)
    if rand_int == 1:
      random_alien = random.choice(self.all_enemies)
      if not random_alien.bullet.active:
        random_alien.shoot()
        self.active_bullets.append(random_alien.bullet)

    # random chance to spawn super alien
    rand_int = random.randint(1, 20)
    if rand_int == 1 and not self.super_alien.active:
      self.super_alien.spawn()

  def recycle_bullet(self, bullet):
    self.active_bullets.remove(bullet)
    bullet.collision()

    












    
