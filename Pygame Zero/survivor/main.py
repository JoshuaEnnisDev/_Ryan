from pgzrun import go

WIDTH = 1792
HEIGHT = 896
TITLE = "Tiny Survivor"

# actors
player = Actor("wizard_purple", (WIDTH / 2, HEIGHT / 2))
player.speed = 3


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


def draw():
    screen.fill((100, 150, 100))
    player.draw()


def update():
    move()
    bound_player()


# last line
go()
