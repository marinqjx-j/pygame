import pygame
import sys

pygame.init()

breite = 400
höhe = 400

screen = pygame.display.set_mode((breite, höhe))
pygame.display.set_caption("Game")

sprite_sheet_image = pygame.image.load("play.png").convert_alpha()

HG = (0, 0, 0)

move_left = False
move_right = False
move_up = False
move_down = False

run = True

player_x = 0
player_y = 0

while run == True:
    screen.fill(HG)
    screen.blit(sprite_sheet_image, (player_x, player_y))
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                move_right = True
            if (event.key == pygame.K_LEFT):
                move_left = True
            if (event.key == pygame.K_UP):
                move_up = True
            if (event.key == pygame.K_DOWN):
                move_down = True
        elif (event.type == pygame.KEYUP):
            if (event.key == pygame.K_RIGHT):
                move_right = False
            if (event.key == pygame.K_LEFT):
                move_left = False
            if (event.key == pygame.K_UP):
                move_up = False
            if (event.key == pygame.K_DOWN):
                move_down = False

        if event.type == pygame.QUIT:
            run = False
        pygame.display.update()
    if (move_right):
        player_x += 0.01
    if (move_left):
        player_x -= 0.01
    if (move_up):
        player_y -= 0.01
    if (move_down):
        player_y += 0.01
    #for quest in
    #if quest go to the kitchen complete:
        #screen.blit(dialogue_background, (dialogue_x, dialogue_y))
        #screen.blit(print("Where's my friend?")
    #if (event.key == pygame.K_space):
        #screen.blit(print("Hi")




pygame.quit
