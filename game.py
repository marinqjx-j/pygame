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
lala_rect = lala.get_rect(topleft=(200,150))

panel_img = pygame.image.load("panel.png").convert_alpha()
knife_img = pygame.image.load("knife.png").convert_alpha()
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (20, 20))

player_lives = 3
lala_lives = 3
lala_alive = True

knives = []
knife_speed = 10
max_knives = 3

player_invulnerable = False
invulnerable_frames = 60
invulnerable_timer = 0

facing = "right"

move_left = False
move_right = False
move_up = False
move_down = False

run = True

while run:
    speed = 5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
        facing = "right"
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
        facing = "left"
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    for k in knives[:]:
        k['rect'].x += k['vx']
        if k['rect'].right < 0 or k['rect'].left > width:
            knives.remove(k)
            continue
        if lala_alive and k['rect'].colliderect(lala_rect):
            lala_lives -= 1
            knives.remove(k)
            if lala_lives <= 0:
                lala_alive = False
            continue

    if lala_alive and lala_rect.colliderect(player_rect):
        if not player_invulnerable:
            player_lives -= 1
            player_invulnerable = True
            invulnerable_timer = invulnerable_frames

    if player_invulnerable:
        invulnerable_timer -= 1
        if invulnerable_timer <= 0:
            player_invulnerable = False

    screen.blit(HG, HG_rect)
    if lala_alive:
        screen.blit(lala, lala_rect)

    for k in knives:
        screen.blit(knife_img, k['rect'])

    if player_invulnerable and (invulnerable_timer // 6) % 2 == 0:
        pass
    else:
        screen.blit(player, player_rect)

    pygame.draw.rect(screen, (172, 147, 98), box, width=2)

    if player_rect.colliderect(box):
        if keys[pygame.K_SPACE] and space_released:
            space_released = False
            index = (index + 1) if (index + 1) != len(text_renders) else 0
        elif not keys[pygame.K_SPACE]:
            space_released = True
    else:
        index = -1

    if index != -1:
        text_surface = text_renders[index]
        padding = 10

        panel_w = text_surface.get_width() + padding * 2
        panel_h = text_surface.get_height() + padding * 2

        panel = pygame.transform.smoothscale(panel_img, (panel_w, panel_h))
        panel.blit(text_surface, (padding, padding))

        panel_x = (width - panel_w) // 2
        panel_y = height - panel_h - 20
        screen.blit(panel, (panel_x, panel_y))

    for i in range(player_lives):
        x = 10 + i * (20 + 5)
        y = 10
        screen.blit(heart_img, (x, y))

    lala_text = font.render(f"Lala: {lala_lives if lala_alive else 0}", True, (200, 50, 50))
    screen.blit(lala_text, (width - 10 - lala_text.get_width(), 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and len(knives) < max_knives:
                k_rect = knife_img.get_rect(center=player_rect.center)
                vx = knife_speed if facing == "right" else -knife_speed
                if vx > 0:
                    k_rect.left = player_rect.right
                else:
                    k_rect.right = player_rect.left
                knives.append({'rect': k_rect, 'vx': vx})

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
