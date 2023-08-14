from pgzrun import go


# add fly

WIDTH = 800
HEIGHT = 400
TITLE = 'Runner'
MAX_SPEED = 20

# player actor
player = Actor('player/player_walk_1')
player.bottom = 305
player.left = 20
gravity = 0

# snail actor
snail = Actor('snail/snail1')
snail.left = 600
snail.bottom = 305
snail_timer = 30
snail_speed = 4

game_started = False
game_over = False
score = 0

BOX = Rect((300, 200), (250, 160))


def draw():
    if not game_started and not game_over:
        screen.fill("blue")
        screen.blit('player/player_stand', (375, 200))
        screen.draw.text(
            "Press space to start",
            (250, 150),
            fontsize=50,
            fontname='pixeltype',
            color=(255, 255, 255)
        )
    elif game_over:
        screen.fill('black')
        screen.draw.filled_rect(BOX, 'red')
        screen.draw.text(
            "Game Over",
            (325, 220),
            fontsize=50,
            fontname='pixeltype',
            color='#FFFF00'
        )
        screen.draw.text(
            f"Final Score:{score}",
            (325, 280),
            fontsize=50,
            fontname='pixeltype',
            color='#FFFF00'
        )
    else:
        screen.blit('sky', (0, 0))
        screen.blit('ground', (0, 300))
        screen.draw.text(
            f"Score: {score}",
            (350, 40),
            fontsize=50,
            fontname='pixeltype',
            color='#555555'
        )
        player.draw()
        snail.draw()


def on_key_down():
    global gravity
    if game_started and keyboard.space and player.bottom >= 305:
        gravity = -20
        player.image = 'player/jump'


def update():
    global game_started
    global game_over
    global gravity
    global snail_timer
    global snail_speed
    global score

    if snail.colliderect(player):
        game_over = True

    # stuff that hapens when game is running
    if game_started and not game_over:
        # player logic
        gravity += 1
        player.y += gravity
        if player.bottom >= 305:
            player.bottom = 305

        snail_speed = min(5 + score / 12, MAX_SPEED)

        # snail logic
        snail_timer -= 1
        snail.x -= snail_speed
        if snail_timer <= 0:
            snail_timer = 30
            if snail.image == 'snail/snail1':
                snail.image = 'snail/snail2'
            else:
                snail.image = 'snail/snail1'

        if snail.right <= 0:
            snail.left = WIDTH
            score += 1

    if not game_started and keyboard.space:
        game_started = True


go()
