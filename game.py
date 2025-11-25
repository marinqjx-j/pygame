import pygame
import sys
import time

pygame.init()

width = 1250
height = 770

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

player = pygame.image.load("play.png").convert_alpha()
player = pygame.transform.smoothscale(player, (125, 200))
player_rect = player.get_rect(topleft=(0, 0))

clock = pygame.time.Clock()

box = pygame.Rect(300, 200, 100, 100)


def display_quest_box():
    quest_rect = pygame.Rect(100, 100, 1050, 570)
    pygame.draw.rect(screen, (246, 194, 86), quest_rect)


font = pygame.font.SysFont('Times New Roman', 20)
first_dialogue = ["Where's my friend?", "Hi.", "What are you?!"]
postfight_dialogue = ["I'm a LaLa and I'm trying to help you. Let me explain first.", "Okay, fine. What do you wanna help me with?", "I know, what happened to your friend. I used to work for this guy called Mr. Labufi. He's the one who kidnapped your friend.", "What? Why?! And where is he?",
                      "Well, Mr. Labufi wants all the LaLas in the world to work for him. And your friend, he knows their locations. I don't know where he is, can you help me find him and save the LaLas?", "What even are LaLas?", "It's my species. We're basically creatures with magical abilities.", "Fine, I'll help you."]
text_renders = [font.render(text, True, (172, 147, 98))
                for text in first_dialogue]

room1_bg = pygame.image.load("room_of_player.png").convert_alpha()

lala_img = pygame.image.load("lala.png").convert_alpha()

panel_img = pygame.image.load("panel.png").convert_alpha()
knife_img = pygame.image.load("knife.png").convert_alpha()
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (20, 20))
cactusfruit_img = pygame.image.load("cactusfruit.png").convert_alpha()
slot_img = pygame.image.load("slot.png").convert_alpha()
quest_button = pygame.image.load("quest_button.png").convert_alpha()

is_quest_box_shown = False

rooms = [
    {
        "bg": room1_bg,
        "has_lala": True,
        "lala_pos": (200, 150),
        "lala_lives": 3,
    },
]

current_room = 0

lala_lives = 0
lala_alive = False
lala_rect = lala_img.get_rect(topleft=(0, 0))

player_lives = 3
max_player_lives = 3

knives = []
knife_speed = 10
max_knives = 3

player_invulnerable = False
invulnerable_frames = 60
invulnerable_timer = 0

facing = "right"

run = True

title_font = pygame.font.SysFont('Times New Roman', 64)
instr_font = pygame.font.SysFont('Times New Roman', 28)

INV_SLOTS = 5
SLOT_SIZE = 64
SLOT_SPACING = 10
slot_img = pygame.transform.smoothscale(slot_img, (SLOT_SIZE, SLOT_SIZE))
knife_inv_img = pygame.transform.smoothscale(
    knife_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))
food_inv_img = pygame.transform.smoothscale(
    cactusfruit_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))

item_imgs = [knife_inv_img, food_inv_img]
for i in range(INV_SLOTS - len(item_imgs)):
    empty = pygame.Surface(
        (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)), pygame.SRCALPHA)
    item_imgs.append(empty)

inventory = [None] * INV_SLOTS
equipped_index = 0

dropped_items = [
    {
        'type': 0,
        'rect': knife_img.get_rect(topleft=(500, 400)),
        'img': knife_img
    },
    {
        'type': 1,
        'rect': cactusfruit_img.get_rect(topleft=(700, 400)),
        'img': cactusfruit_img
    }
]

game_state = "start_screen"
dialogue_index = 0
space_released = True
dialogue_done = False


def reset_game_state():
    global current_room, lala_lives, lala_alive, lala_rect, player_lives
    global knives, player_rect, facing, player_invulnerable, invulnerable_timer
    global equipped_index, inventory, dropped_items, game_state, dialogue_index, space_released, dialogue_done
    current_room = 0
    room = rooms[current_room]
    lala_lives = room.get("lala_lives", 0)
    lala_alive = bool(room.get("has_lala", False))
    lala_rect.topleft = room.get("lala_pos", (0, 0))
    player_lives = max_player_lives
    knives = []
    player_rect.topleft = (0, 0)
    facing = "right"
    player_invulnerable = False
    invulnerable_timer = 0
    equipped_index = 0
    inventory = [None] * INV_SLOTS
    dropped_items = [
        {
            'type': 0,
            'rect': knife_img.get_rect(topleft=(500, 400)),
            'img': knife_img
        },
        {
            'type': 1,
            'rect': cactusfruit_img.get_rect(topleft=(700, 400)),
            'img': cactusfruit_img
        }
    ]
    game_state = "start_screen"
    dialogue_index = 0
    space_released = True
    dialogue_done = False


reset_game_state()


def enter_room(new_room_index, from_right):
    global current_room, lala_lives, lala_alive, lala_rect
    current_room = new_room_index
    room = rooms[current_room]
    lala_lives = room.get("lala_lives", 0)
    lala_alive = bool(room.get("has_lala", False))
    lala_rect.topleft = room.get("lala_pos", (0, 0))
    if from_right:
        player_rect.right = width
    else:
        player_rect.left = 0


def get_inventory_rects():
    total_width = INV_SLOTS * SLOT_SIZE + (INV_SLOTS - 1) * SLOT_SPACING
    start_x = (width - total_width) // 2
    y = height - SLOT_SIZE - 10
    rects = []
    for i in range(INV_SLOTS):
        x = start_x + i * (SLOT_SIZE + SLOT_SPACING)
        rects.append(pygame.Rect(x, y, SLOT_SIZE, SLOT_SIZE))
    return rects


def render_inventory(surface, mouse_pos, equipped):
    rects = get_inventory_rects()
    for i, rect in enumerate(rects):
        if i == equipped:
            pygame.draw.rect(surface, (255, 220, 0), rect.inflate(6, 6), 4)
        elif rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (100, 200, 255), rect.inflate(4, 4), 4)
        surface.blit(slot_img, rect.topleft)
        idx = inventory[]
        if idx is not None:
            item_rect = item_imgs[idx].get_rect()
            item_rect.center = rect.center
            surface.blit(item_imgs[idx], item_rect)


speed = 5

quest_button_x = 1115
quest_button_y = 50
screen.blit(quest_button, (quest_button_x, quest_button_y))
mouse = pygame.mouse.get_pos()

while run:
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if quest_button_x <= mouse[0] <= quest_button_x + 125 and quest_button_y <= mouse[1] <= quest_button_y + 75:
                is_quest_box_shown = not is_quest_box_shown
        if game_state == "start_screen":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                game_state = "main"
                dialogue_index = 0
                space_released = False
        elif game_state == "intro":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_released:
                dialogue_index += 1
                space_released = False
                if dialogue_index >= len(first_dialogue):
                    game_state = "main"
                    dialogue_done = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_released = True
        elif game_state == "main":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(knives) < max_knives:
                    if inventory[equipped_index] == 0:
                        k_rect = knife_img.get_rect(center=player_rect.center)
                        vx = knife_speed if facing == "right" else -knife_speed
                        if vx > 0:
                            k_rect.left = player_rect.right
                        else:
                            k_rect.right = player_rect.left
                        knives.append({'rect': k_rect, 'vx': vx})
                if lala_lives == 1:
                    game_state = "postfight_dialogue"
        elif game_state == "postfight_dialogue":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_released:
                dialogue_index += 1
                space_released = False
                if dialogue_index >= len(postfight_dialogue):
                    game_state = "maintwo"
                    dialogue_done = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_released = True
            if event.key == pygame.K_e:
                to_pick = None
                for i, item in enumerate(dropped_items):
                    if player_rect.colliderect(item['rect']):
                        to_pick = i
                        break
                if to_pick is not None:
                    free_slot = None
                    for idx, slot in enumerate(inventory):
                        if slot is None:
                            free_slot = idx
                            break
                    if free_slot is not None:
                        inventory[free_slot] = dropped_items[to_pick]['type']
                        dropped_items.pop(to_pick)
            if event.key == pygame.K_g:
                drop_item = inventory[equipped_index]
                if drop_item is not None:
                    px = player_rect.centerx - \
                        item_imgs[drop_item].get_width()//2
                    py = player_rect.bottom - item_imgs[drop_item].get_height()
                    rect = item_imgs[drop_item].get_rect(topleft=(px, py))
                    dropped_items.append({
                        'type': drop_item,
                        'rect': rect,
                        'img': item_imgs[drop_item] if drop_item < len(item_imgs) else knife_img
                    })
                    inventory[equipped_index] = None
            if event.key == pygame.K_f and inventory[equipped_index] == 1:
                player_lives = min(player_lives + 1, max_player_lives)
                inventory[equipped_index] = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rects = get_inventory_rects()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        equipped_index = i

    if game_state == "start_screen":
        screen.fill((0, 0, 0))
        title_surf = title_font.render(
            "Save the LaLas!", True, (255, 255, 255))
        instr_surf = instr_font.render(
            "Click Enter oder Space to start...", True, (200, 200, 200))
        screen.blit(
            title_surf, ((width - title_surf.get_width())//2, height//3))
        screen.blit(
            instr_surf, ((width - instr_surf.get_width())//2, height//3 + 100))
        pygame.display.update()
        clock.tick(60)
        continue

    screen.blit(rooms[current_room]["bg"], (0, 0))

    if game_state == "dialogue":
        screen.blit(lala_img, lala_rect)
        screen.blit(player, player_rect)
        if dialogue_index < len(text_renders):
            text_surface = text_renders[dialogue_index]
            padding = 12
            panel_w = text_surface.get_width() + padding * 2
            panel_h = text_surface.get_height() + padding * 2
            panel = pygame.transform.smoothscale(panel_img, (panel_w, panel_h))
            panel.blit(text_surface, (padding, padding))
            panel_x = (width - panel_w) // 2
            panel_y = height - panel_h - 20
            screen.blit(panel, (panel_x, panel_y))
        pygame.display.update()
        clock.tick(60)
        continue

    if game_state == "main":
        if lala_alive and rooms[current_room]["has_lala"]:
            screen.blit(lala_img, lala_rect)

        for k in knives[:]:
            k['rect'].x += k['vx']
            if k['rect'].right < 0 or k['rect'].left > width:
                knives.remove(k)
                continue
            if lala_alive and k['rect'].colliderect(lala_rect):
                lala_lives = max(0, lala_lives - 1)
                knives.remove(k)
                continue

        if lala_alive and lala_rect.colliderect(player_rect):
            if not player_invulnerable:
                player_lives -= 1
                player_lives = max(0, player_lives)
                player_invulnerable = True
                invulnerable_timer = invulnerable_frames

        if player_invulnerable:
            invulnerable_timer -= 1
            if invulnerable_timer <= 0:
                player_invulnerable = False

        if player_lives <= 0:
            reset_game_state()
            continue

        if dialogue_done and lala_alive:
            for i in range(lala_lives):
                x = width - 10 - heart_img.get_width() - i * (heart_img.get_width() + 5)
                y = 10
                screen.blit(heart_img, (x, y))
            if lala_lives <= 0:
                lala_alive = False

        for k in knives:
            screen.blit(knife_img, k['rect'])

        if player_invulnerable and (invulnerable_timer // 6) % 2 == 0:
            pass
        else:
            screen.blit(player, player_rect)

        pygame.draw.rect(screen, (172, 147, 98), box, width=2)

        heart_w = heart_img.get_width()
        spacing = 5
        for i in range(player_lives):
            x = 10 + i * (heart_w + spacing)
            y = 10
            screen.blit(heart_img, (x, y))

        pygame.mouse.set_visible(True)
        # @TODO add fix arguments
        # render_inventory(screen, mouse_pos, equipped_index)

        for item in dropped_items:
            screen.blit(item['img'], item['rect'])

    if game_state == "main":
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

        if player_rect.left >= width:
            if current_room < len(rooms) - 1:
                enter_room(current_room + 1, from_right=False)
            else:
                player_rect.right = width - 1

        if player_rect.right <= 0:
            if current_room > 0:
                enter_room(current_room - 1, from_right=True)
            else:
                player_rect.left = 0

        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > height:
            player_rect.bottom = height

    if is_quest_box_shown:
        display_quest_box()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
