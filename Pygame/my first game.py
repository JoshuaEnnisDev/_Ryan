#import pygame
import pygame

#initalize pygame
pygame.init()

#Create the main surface
WIDTH = 800
HEIGHT = 400
DS = pygame.display.set_mode((WIDTH, HEIGHT)) 

#create background surfaces
sky_surf = pygame.image.load('graphics/Sky.png')
ground_surf = pygame.image.load('graphics/ground.png')

#create a font
font = pygame.font.Font('font/Pixeltype.ttf', 50)
text_surf = font.render("Runner", False,"black")
#Event loop
running = True
count = 0
while running:
    print(count)
    #run through all the events
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    DS.blit(sky_surf,(0,0))
    DS.blit(ground_surf, (0,300))
    DS.blit(text_surf, (350,40))
    pygame.display.update()

pygame.quit()




