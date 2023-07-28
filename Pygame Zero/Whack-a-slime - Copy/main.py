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

#helper variables
speed = 60
timer = speed
score = 0
is_hit = False

def place_slime():
  rand_num = randint(1,3)
  if rand_num == 1:
    slime.midbottom = hole1.center
  elif rand_num == 2:
    slime.midbottom = hole2.center
  elif rand_num == 3:
    slime.midbottom = hole3.center
  
def draw():
  screen.fill('green')
  hole1.draw()
  hole2.draw()
  hole3.draw()
  slime.draw()
  screen.draw.text(f"Score:{score}",(10,10), fontsize=35, color='black')
  hammer.draw()
  
def on_mouse_down(pos):
  global score
  global is_hit
  if slime.collidepoint(pos) and not is_hit:
    slime.image = 'slime_hurt'
    is_hit = True
    score += 1

def on_mouse_move(pos):
  hammer.center = pos
  

def update():
  global timer
  global is_hit
  hide_mouse()
  timer -= 1
  
  if timer <= 0:
    place_slime()
    is_hit = False
    timer=speed
    slime.image = 'slime'
  
go()