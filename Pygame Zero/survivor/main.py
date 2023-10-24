from pgzrun import go
import math

WIDTH = 1792
HEIGHT = 896
TITLE = "Tiny Survivor"

# actors
player = Actor("wizard", (WIDTH / 2, HEIGHT / 2))
player.speed = 3

axes = []
axe_timer = 180
radius = 1
direction = 0

axe = Actor("axe", player.pos)

for i in range(3):
    axe = Actor("axe", player.pos)
    axes.append(axe)
    axe.x = 100
    axe.y = player.y + 90 * i


def move():
    if keyboard.a:
        # move left
        player.x -= player.speed
    elif keyboard.w:
        player.y -= player.speed
    # needs to be completed


def bound_player():
    if player.left <= 0:
        player.left = 0
    elif player.right > WIDTH:
        player.right = WIDTH
    # needs to be completed


def make_axe():
    global axe_timer
    global radius
    axe_timer -= 1
    if axe_timer <= 0:
        if len(axes) > 0:
            axes.pop(0)
        axe_timer = 180
        axe = Actor("axe", player.pos)
        radius = 0
        axes.append(axe)


def draw():
    screen.blit("dungeon1", (0, 0))
    player.draw()
    if len(axes) > 0:
        axes[0].draw()


def circle_player(actors, speed):
    global direction
    direction += speed
    direction = min(direction, 6.28)
    if direction >= 6.28:
        direction = 0
    for i, actor in enumerate(actors):
        
        actor.x = player.x + 100 * math.cos(direction)
        actor.y = player.y + 100 * math.sin(direction)


def update():
    move()
    bound_player()
    make_axe()
    global radius
    global direction
    direction += 0.05
    radius += 0.5
    direction = min(6.28, direction)
    if direction >= 6.28:
        direction = 0
    axes[0].x = player.x + radius * math.cos(direction)
    axes[0].y = player.y + radius * math.sin(direction)

# last line
go()
