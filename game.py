import pygame
import sys

pygame.init()

breite = 400
höhe = 400

screen = pygame.display.set_mode((breite, höhe))
pygame.display.set_caption("Game")

sprite_sheet_image = pygame.image.load("play.png").convert_alpha()

background = (0, 0, 0)

isMovingLeft = False
isMovingRight = False
isMovingUp = False
isMovingDown = False

run = True

player_coord_x = 0
player_coord_y = 0

while run == True:
    screen.fill(background)
    screen.blit(sprite_sheet_image, (player_coord_x, player_coord_y))
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                isMovingRight = True
            if (event.key == pygame.K_LEFT):
                isMovingLeft = True
            if (event.key == pygame.K_UP):
                isMovingUp = True
            if (event.key == pygame.K_DOWN):
                isMovingDown = True
        elif (event.type == pygame.KEYUP):
            if (event.key == pygame.K_RIGHT):
                isMovingRight = False
            if (event.key == pygame.K_LEFT):
                isMovingLeft = False
            if (event.key == pygame.K_UP):
                isMovingUp = False
            if (event.key == pygame.K_DOWN):
                isMovingDown = False

        if event.type == pygame.QUIT:
            run = False
        pygame.display.update()
    if (isMovingRight):
        player_coord_x += 0.01
    if (isMovingLeft):
        player_coord_x -= 0.01
    if (isMovingUp):
        player_coord_y -= 0.01
    if (isMovingDown):
        player_coord_y += 0.01
    #for quest in
    #if quest go to the kitchen complete:
        #screen.blit(dialogue_background, (dialogue_x, dialogue_y))
        #screen.blit(print("Where's my friend?")
    #if (event.key == pygame.K_space):
        #screen.blit(print("Hi")




pygame.quit
