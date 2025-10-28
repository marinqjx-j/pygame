import pygame
import sys
import time

pygame.init()

width = 400
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

player = pygame.image.load("play.png").convert_alpha()
player_rect = player.get_rect(topleft=(0, 0))

clock = pygame.time.Clock()

box = pygame.Rect(300, 200, 100, 100)

font = pygame.font.SysFont('Times New Roman', 20)
dialogue = ["Where's my friend?", "Hi.", "What are you?!"]
text_renders = [font.render(text, True, (172,147, 98)) for text in dialogue]
index = -1
space_released = True

HG = pygame.image.load("raum_von_player.png").convert_alpha()
HG_rect = HG.get_rect(topleft=(0, 0))

lala = pygame.image.load("lala.png").convert_alpha()
lala_rect = lala.get_rect(topleft=(0,0))

#

move_left = False
move_right = False
move_up = False
move_down = False

run = True

while run:
    # movement
    speed = 5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    screen.blit(HG, HG_rect)
    screen.blit(lala, lala_rect)
    screen.blit(player, player_rect)
    pygame.draw.rect(screen, (172, 147, 98), box, width=2)

    # dialogue logic
    if player_rect.colliderect(box):
        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            index = (index + 1) if (index + 1) != len(text_renders) else 0
        elif not keys[pygame.K_SPACE]:
            space_released = True
    else:
        index = -1

    # dialogue background(panel)
    if index != -1:
        text_surface = text_renders[index]
        padding = 10

        panel_w = text_surface.get_width() + padding * 2
        panel_h = text_surface.get_height() + padding * 2

    panel_img = pygame.image.load("panel.png").convert_alpha()
    panel = pygame.transform.smoothscale(panel_img, (panel_w, panel_h))

    panel.blit(text_surface, (padding, padding))

    panel_x = (width - panel_w) // 2
    panel_y = height - panel_h - 20
    screen.blit(panel, (panel_x, panel_y))

    #if knife_rect.colliderect(lala):
         #lala verliet ein leben

    #if lala_rect.colliderect(player):
         #player verliert ein leben

    #if leben_player < 1:
         #game over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
