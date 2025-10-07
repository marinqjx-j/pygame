import pygame
import sys
import time

pygame.init()

breite = 600
höhe = 600

screen = pygame.display.set_mode((breite, höhe))
pygame.display.set_caption("Game")

player = pygame.image.load("play.png").convert_alpha()

clock = pygame.time.Clock()

box = pygame.Rect(300, 200, 100, 100)

font = pygame.font.SysFont('Times New Roman', 20)
dialogue = ["Where's my friend?", "Hi.", "What are you?!"]
text_renders = [font.render(text, True, (0, 0, 255)) for text in dialogue]
index = -1
space_released = True

HG = (0, 0, 0)

move_left = False
move_right = False
move_up = False
move_down = False

run = True

while run == True:
    screen.fill(HG)
    pygame.draw.rect(screen, (0, 255, 0), box, width=2)

    keys = pygame.key.get_pressed()

    if player.colliderect(box):
        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            index = (index + 1) if (index + 1) != len(text_renders) else 0
        elif not keys[pygame.K_SPACE]:
            space_released = True
    else:
        index = -1

    if index != -1:
        screen.blit(text_renders[index], (0, 0))


    screen.blit(player, (0,0))
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RIGHT):
                move_right = True
            if(event.key == pygame.K_LEFT):
                move_left = True
            if(event.key == pygame.K_UP):
                move_up = True
            if(event.key == pygame.K_DOWN):
                move_down = True
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RIGHT):
                move_right = True
            if(event.key == pygame.K_LEFT):
                move_left = True
            if(event.key == pygame.K_UP):
                move_up = True
            if(event.key == pygame.K_DOWN):
                move_down = True
   

        if event.type == pygame.QUIT:
            run = False
            

        pygame.display.update()

pygame.quit()

