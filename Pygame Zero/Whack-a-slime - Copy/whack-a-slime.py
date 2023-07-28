import pgzrun
import random
from pgzhelper import *


WIDTH = 600
HEIGHT = 400
score = 0
hide_mouse()

holes = [
  [],
  [],
  [],
  []
]

for row in range(4):
  for col in range(3):
    hole = Actor('hole')
    holes[row].append(hole)


mole = Actor('slime', (-100,0))
red_slime = Actor('red_slime', (-100,0))
hammer = Actor('hammer')
is_hit = False

COOLDOWN = 60
timer = COOLDOWN

def reset_slime():
  mole.image = 'slime'

def on_mouse_down(pos):
  global score
  global is_hit
  hammer.angle -= 45
  
  if mole.collidepoint(pos) and not is_hit:
    is_hit = True
    mole.image = 'slime_hurt'
    sounds.hit3.play()
    animate(mole, pos=(mole.x, mole.y + 50), tween='accelerate')
    clock.schedule_unique(reset_slime, 0.5)
    score += 1
  else:
    sounds.whoosh2.play()
    
def on_mouse_up():
  hammer.angle += 45
  
def on_mouse_move(pos):
  hammer.center = pos
  
def place_actor(actor):
  rand_row = random.randint(0,3)
  rand_col = random.randint(0,2)
  
  hole = holes[rand_row][rand_col]
  
  actor.x = hole.x
  actor.y = hole.y - 10
  animate(actor, pos=(hole.x, hole.y - 30), tween='decelerate')

def draw():
  
  screen.fill('yellow')
  screen.draw.text(f"Score: {score}", (5,10), color='black', fontsize=32)
  for row in range(4):
    for col in range(3):
      holes[row][col].y = 100 * row + 75
      holes[row][col].x = 150 * col + 150
      holes[row][col].draw()
    
  mole.draw()
  red_slime.draw()
  hammer.draw()
  
def update():
  
  global timer
  global is_hit
  
  timer -= 1
  if timer <= 0:
    print("yo")
    place_actor(mole)
    place_actor(red_slime)
    is_hit = False
    timer = 60

pgzrun.go()