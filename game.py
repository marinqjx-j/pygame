import pygame
import sys

pygame.init()

screen_width = 1250
screen_height = 770
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Game")

player = pygame.image.load("play.png").convert_alpha()
player = pygame.transform.smoothscale(player, (100, 100))
player_rect = player.get_rect(topleft=(0, 0))

framerate_timer = pygame.time.Clock()

box = pygame.Rect(300, 200, 100, 100)

# dialogue
font = pygame.font.SysFont('Times New Roman', 20)
dialogue = ["Where's my friend?", "Hi.", "What are you?!"]
text_renders = [font.render(text, True, (172, 147, 98)) for text in dialogue]
index = -1
space_released = True

room1_bg = pygame.image.load("raum_von_player.png").convert_alpha()

lala_img = pygame.image.load("lala.png").convert_alpha()

panel_img = pygame.image.load("panel.png").convert_alpha()
knife_img = pygame.image.load("knife.png").convert_alpha()
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (20, 20))

rooms = [
    {
        "bg": room1_bg,
        "has_lala": True,
        "lala_pos": (200, 150),
        "lala_lives": 3,
    },
    # {
    # "bg": room2_bg,
    # "has_lala": False,
    # "lala_pos": (0, 0),
    # "lala_lives": 0,
    # },
]

current_room = 0

lala_lives = rooms[current_room]["lala_lives"]
lala_alive = rooms[current_room]["has_lala"]
lala_rect = lala_img.get_rect(topleft=rooms[current_room]["lala_pos"])

player_lives = 3

knives = []
knife_speed = 10
max_knives = 3

player_invulnerable = False
invulnerable_frames = 60
invulnerable_timer = 0

facing = "right"

run = True

# change room


def enter_room(new_room_index, from_right):
    """Switch to new room index and place player on the entering edge.
       from_right True means player came from the right (i.e., they walked left off the left edge),
       so place player on the right edge in the new room. Otherwise place player on the left edge.
    """
    global current_room, lala_lives, lala_alive, lala_rect
    current_room = new_room_index
    room = rooms[current_room]

    lala_lives = room.get("lala_lives", 0)
    lala_alive = bool(room.get("has_lala", False))
    lala_rect.topleft = room.get("lala_pos", (0, 0))

    if from_right:

        player_rect.right = screen_width
    else:

        player_rect.left = 0


# main loop
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

    if player_rect.left >= screen_width:

        if current_room < len(rooms) - 1:
            enter_room(current_room + 1, from_right=False)
        else:

            player_rect.right = screen_width - 1

    if player_rect.right <= 0:
        if current_room > 0:
            enter_room(current_room - 1, from_right=True)
        else:
            player_rect.left = 0

    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > screen_height:
        player_rect.bottom = screen_height

    for k in knives[:]:
        k['rect'].x += k['vx']
        if k['rect'].right < 0 or k['rect'].left > screen_width:
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

    screen.blit(rooms[current_room]["bg"], (0, 0))

    if lala_alive and rooms[current_room]["has_lala"]:
        screen.blit(lala_img, lala_rect)

    for k in knives:
        screen.blit(knife_img, k['rect'])

    if player_invulnerable and (invulnerable_timer // 6) % 2 == 0:
        pass
    else:
        screen.blit(player, player_rect)

    pygame.draw.rect(screen, (172, 147, 98), box, width=2)

    # quests
    # quests: ["Look in your friends room.", "Go to the kitchen.", "Get the knife.", "Follow LaLa."]
    # for i in quests:
    # quest_complete = False
    #

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

        panel_x = (screen_width - panel_w) // 2
        panel_y = screen_height - panel_h - 20
        screen.blit(panel, (panel_x, panel_y))

    heart_w = heart_img.get_width()
    spacing = 5
    for i in range(player_lives):
        x = 10 + i * (heart_w + spacing)
        y = 10
        screen.blit(heart_img, (x, y))

    for i in range(lala_lives):
        x = screen_width - 10 - heart_w - i * (heart_w + spacing)
        y = 10
        screen.blit(heart_img, (x, y))

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

    game_framerate_in_ms = 60
    framerate_timer.tick(game_framerate_in_ms)

pygame.quit()
sys.exit()
