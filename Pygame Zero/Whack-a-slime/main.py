from pgzrun import go
from random import randint
from pgzhelper import *

#Screen setup
WIDTH = 600
HEIGHT = 400

#Actors
slime = Actor('slime', (-1000, 0))
hammer = Actor('hammer')

hole1 = Actor('hole', (200, 100))
hole2 = Actor('hole', (350, 100))
hole3 = Actor('hole', (500, 100))

holes = []

for col in range(3):
  for row in range(3):
    hole = Actor('hole')
    hole.x = 200 + 150 * row
    hole.y = 100 + 100 * col
    print(hole.pos)
    holes.append(hole)


#helper variables
speed = 60
timer = speed
score = 0
is_hit = False


hide_mouse()

def place_slime():
  rand = randint(0, len(holes) - 1)
  hole = holes[rand]
  slime.midbottom = hole.pos

  animate(slime, pos=(slime.x, slime.y - 30), tween='decelerate')
  
def draw():
  screen.fill('green')
  for hole in holes:
    hole.draw()
    
  slime.draw()
  screen.draw.text(f"Score:{score}",(10,10), fontsize=35, color='black')
  hammer.draw()
  
def on_mouse_down(pos):
  global score
  global is_hit
  hammer.angle = -45
  if slime.collidepoint(pos) and not is_hit:
    slime.image = 'slime_hurt'
    animate(slime, pos=(slime.x, slime.y + 50), tween='accelerate')
    sounds.hit3.play()
    is_hit = True
    score += 1
  else:
    sounds.whoosh2.play()
    
def on_mouse_up():
  hammer.angle = 0

def on_mouse_move(pos):
  hammer.center = pos
  

def update():
  global timer
  global is_hit
  timer -= 1
  if timer <= 0:
    place_slime()
    is_hit = False
    timer=speed
    slime.image = 'slime'
  
go()