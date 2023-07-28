from pgzrun import go

WIDTH = 800
HEIGHT = 400

TITLE = 'Runner'

#player actor
player = Actor('player/player_walk_1')
player.bottom = 305
player.left = 20

#snail actor
snail = Actor('snail/snail1')
#snail.right = WIDTH - 20
snail.bottom = 305

game_started = False

def draw():

    if not game_started:
        screen.fill("blue")
        screen.blit('player/player_stand', (375,200))
        screen.draw.text("Press space to start", 
                        (250, 150),
                        fontsize = 50,
                        fontname = 'pixeltype',
                        color = (255,255,255))
    else:
        screen.blit('sky', (0,0))
        screen.blit('ground',(0,300) )
        screen.draw.text("My game", 
                        (350, 40), 
                        fontsize = 50, 
                        fontname = 'pixeltype', 
                        color = '#555555'
                    )

        player.draw()
        snail.draw()

def update():
    # tells python we are talking about the
    # variable we made outside of the function
    global game_started 

    if not game_started and keyboard.space:
        game_started = True

go()