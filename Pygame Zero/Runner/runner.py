from pgzrun import go

WIDTH = 800
HEIGHT = 400

TITLE = 'Runner'

#player actor
player = Actor('player/player_walk_1')
player.bottom = 305
player.left = 20
gravity = 0

#snail actor
snail = Actor('snail/snail1')
snail.left = WIDTH
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

def on_key_down():
    global gravity
    if keyboard.space and player.bottom >= 305:
            gravity = -20

def update():
    global game_started
    global gravity
    
    #stuff that hapens when game is running
    if game_started:
        #player logic
        gravity += 1
        player.y += gravity
        if player.bottom >= 305:
            player.bottom = 305
            
        #snail logic
        snail.x -= 4
        if snail.right <= 0:
            snail.left = WIDTH
        
    if not game_started and keyboard.space:
        game_started = True

go()