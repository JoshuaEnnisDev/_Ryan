#import pygame
import pygame

#initalize pygame
pygame.init()

#Create the main surface
WIDTH = 800
HEIGHT = 500
#main screen
#DISPLAY_SURFACE
DS = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Change title")
#pygame.display.set_icon()

#Event loop
running = True

while running:
    #run through all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


pygame.quit()




