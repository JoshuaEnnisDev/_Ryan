from pgzrun import go
from pgzhelper import *
import random
import math

WIDTH = 600
HEIGHT = 600

paddle1 = Actor('paddle_lego')
paddle1.left = 0
paddle1.y = HEIGHT / 2

paddle2 = Actor('paddle_caution')
paddle2.right = WIDTH
paddle2.y = HEIGHT / 2

ball = Actor('ball_sky', (WIDTH / 2, HEIGHT / 2))

ball_speed = 4
ball.direction = 45
print(ball.direction)
def draw():
    screen.clear()
    paddle1.draw()
    paddle2.draw()
    ball.draw()

def update():
    ball.move_in_direction(ball_speed)

go()