from turtle import Screen
from player_ship import PlayerShip
from invaders import Invaders
from barriers import Barriers
from scoreboard import Scoreboard
import time 

SCREEN_TOP = 490
SCREEN_BOTTOM = -490
SHIP_BULLET_COLLISION_DISTANCE = 30
ALIEN_BULLET_COLLISION_DISTANCE = 40
SUPER_BULLET_COLLISION_DISTANCE = 40
BARRIER_COLLISION_DISTANCE = 60
SUPER_ALIEN_COLLISION_DISTANCE = 60
SCREEN_UPDATE_TIMER = 0.05
START_TIME = 3

screen = Screen()
screen.setup(width=1000, height=1000)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.register_shape("images/spaceship.gif")
screen.register_shape("images/purple-alien.gif")
screen.register_shape("images/green-alien.gif")
screen.register_shape("images/red-alien.gif")
screen.register_shape("images/lives.gif")
screen.register_shape("images/explosion.gif")
screen.register_shape("images/barrier1.gif")
screen.register_shape("images/barrier2.gif")
screen.register_shape("images/barrier3.gif")
screen.register_shape("images/super-alien.gif")
screen.tracer(0)
 
p_ship = PlayerShip()
invaders = Invaders()
barriers = Barriers()
scoreboard = Scoreboard()

key_events = set()
key_event_handlers = {
  "l": p_ship.left,
  "r": p_ship.right,
  "s": p_ship.shoot
}


def process_keys():
  for action in key_events:
    key_event_handlers[action]()


screen.onkeypress(lambda: key_events.add("l"), "Left")
screen.onkeypress(lambda: key_events.add("r"), "Right")
screen.onkeypress(lambda: key_events.add("s"), "space")
screen.onkeyrelease(lambda: key_events.remove("l"), "Left")
screen.onkeyrelease(lambda: key_events.remove("r"), "Right")
screen.onkeyrelease(lambda: key_events.remove("s"), "space")
screen.listen()


def start_game():
  loop_num = 5
  flash_timer = 0.5
  scoreboard.game_start()
  show_text = True

  for _ in range(loop_num):
    screen.update()
    time.sleep(flash_timer)
    if show_text:
      scoreboard.start_text.clear()
    else:
      scoreboard.write_start()
    show_text = not show_text

  scoreboard.remove_start_text()
  p_ship.game_on = True


def reset_screen():
  screen.update()

  for bullet in invaders.active_bullets:
    bullet.collision()
  invaders.active_bullets = []

  for bullet in p_ship.active_bullets:
    p_ship.inactive_bullets.append(bullet)
    bullet.collision()
  p_ship.active_bullets = []

  p_ship.reset_pos()
  scoreboard.update_lives()

  if invaders.super_alien.active:
    invaders.super_alien.despawn()

  if scoreboard.lives == 0:
    p_ship.hideturtle()
    p_ship.game_on = False
    scoreboard.game_over("SHIP EXPLODED")
    screen.update()
    return
  else:
    p_ship.shape("images/spaceship.gif")
    time.sleep(2)


start_game()
while p_ship.game_on:
  screen.update()
  time.sleep(SCREEN_UPDATE_TIMER)

  reset = False
  p_ship_collisions = []
  invaders_collisions = []

  # process player input
  process_keys()

  # move player bullets
  if len(p_ship.active_bullets) > 0:
    for bullet in p_ship.active_bullets:
      bullet.move()

      # - CHECK COLLISIONS
      if bullet.cur_y >= SCREEN_TOP:
        p_ship_collisions.append(bullet)
        break
      
      if invaders.super_alien.active and \
      bullet.distance(invaders.super_alien) <= SUPER_ALIEN_COLLISION_DISTANCE:
        invaders.alien_hit(invaders.super_alien)
        p_ship_collisions.append(bullet)
        scoreboard.update_score(invaders.super_alien.points)
        break

      for alien in invaders.all_enemies:
        if bullet.distance(alien) <= SHIP_BULLET_COLLISION_DISTANCE:
          invaders.alien_hit(alien)
          p_ship_collisions.append(bullet) 
          scoreboard.update_score(alien.points)
          break

      # if bullet hasn't hit any aliens
      if bullet.active:
        for barrier in barriers.all_barriers:
          if bullet.distance(barrier) <= BARRIER_COLLISION_DISTANCE:
            p_ship_collisions.append(bullet)
            break
      
  # shoot alien bullets
  invaders.alien_attack()

  # move alien bullets   
  if len(invaders.active_bullets) > 0:
    for bullet in invaders.active_bullets:
      bullet.move()

      # - CHECK COLLISIONS
      if bullet.cur_y <= SCREEN_BOTTOM:
        invaders_collisions.append(bullet)
        break

      if bullet.distance(p_ship) <= ALIEN_BULLET_COLLISION_DISTANCE:
        p_ship.hit()
        invaders_collisions.append(bullet)

        reset_screen()
        reset = True
        break
    
      for barrier in barriers.all_barriers:
        if bullet.distance(barrier) <= BARRIER_COLLISION_DISTANCE:
          barriers.hit(barrier, bullet.dmg)
          invaders_collisions.append(bullet)
          break

  # check super bullet collision
  super_bullet = invaders.super_alien.bullet
  if super_bullet.active:
    if p_ship.distance(super_bullet.collision_point) <= SUPER_BULLET_COLLISION_DISTANCE:
      p_ship.hit()
      reset_screen()
      reset = True

  if reset:
    continue

  # recycle bullets that hit something
  for bullet in p_ship_collisions:
    p_ship.recycle_bullet(bullet)
  for bullet in invaders_collisions:
    invaders.recycle_bullet(bullet)

  # move aliens
  invaders.move_aliens()

  # check if aliens won
  if invaders.breached:
    p_ship.game_on = False
    scoreboard.game_over("ALIEN BREACH")
    screen.update()

  # check if player won
  if len(invaders.all_enemies) == 0:
    p_ship.game_on = False
    scoreboard.game_won()
    screen.update()


screen.exitonclick()

















