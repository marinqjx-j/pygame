# start
import pygame
import sys
import time
import random

pygame.init()

width = 1250
height = 770

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

player = pygame.image.load("play.png").convert_alpha()
player = pygame.transform.smoothscale(player, (200, 320))
player_rect = player.get_rect(bottomleft=(100, 750))

clock = pygame.time.Clock()

player_frames = ["player.back.1.png", "player.back.2.png", "player.front.1.png", "player.front.2.png",
                 "player.left.1.png", "player.left.2.png", "player.right.1.png", "player.right.2.png"]
active_player_frame_index = 0
player_mode = 0
#0 = 3 + 2 (facing forward) 1 = 0 + 1 (running forward) 2 = 4 + 5 (running left) 3 = 6 + 7 (running right)
count = 0


def display_quest_box():
    quest_rect = pygame.Rect(100, 100, 1050, 570)
    pygame.draw.rect(screen, (246, 194, 86), quest_rect)


# dialogue (setup)
font = pygame.font.SysFont('Times New Roman', 20)
player_header = ["You"]
lala_header = ["LaLa"]
first_dialogue = ["Where's my friend?", "Hi.", "What are you?!"]
postfight_dialogue = [
    "I'm a LaLa and I'm trying to help you. Let me explain first.", "Okay, fine. What do you wanna help me with?",
    "I know, what happened to your friend. I used to work for this guy [...]",
    "Well, Mr. Labufi wants all the LaLas in the world to work for him. And your friend, he knows their locations. I don't know where he is, can you help me find him and save the LaL[...]"
]
text_renders = [font.render(text, True, (172, 147, 98))
                for text in first_dialogue]

# images
room1_bg = pygame.image.load("raum_von_player.png").convert_alpha()
room1_bg = pygame.transform.smoothscale(room1_bg, (width, height))

room2_bg = pygame.image.load("kitchen.png").convert_alpha()
room2_bg = pygame.transform.smoothscale(room2_bg, (width, height))

lala_img = pygame.image.load("lala.png").convert_alpha()

lulu_img = pygame.image.load("lulu.png").convert_alpha()

panel_img = pygame.image.load("panel.png").convert_alpha()
panel_img = pygame.transform.smoothscale(panel_img, (800, 250))
knife_img = pygame.image.load("knife.png").convert_alpha()
spike_img = pygame.image.load("spike.png").convert_alpha()
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (50, 50))
cactusfruit_img = pygame.image.load("cactusfruit.png").convert_alpha()
slot_img = pygame.image.load("slot.png").convert_alpha()
quest_button = pygame.image.load("quest_button.png").convert_alpha()

# scorpion image
try:
    scorpion_img = pygame.image.load("scorpion.png").convert_alpha()
except Exception:
    scorpion_img = pygame.Surface((80, 40), pygame.SRCALPHA)
    scorpion_img.fill((80, 40, 0))
    pygame.draw.circle(scorpion_img, (0, 0, 0), (20, 12), 4)
    pygame.draw.circle(scorpion_img, (0, 0, 0), (60, 12), 4)
scorpion_img = pygame.transform.smoothscale(scorpion_img, (100, 50))
scorpion_rect = scorpion_img.get_rect(topleft=(0, 0))


wood_img = pygame.image.load("wood.png").convert_alpha()
stone_img = pygame.image.load("stone.png").convert_alpha()
axe_img = pygame.image.load("axe.png").convert_alpha()

is_quest_box_shown = False

rooms = [
    {
        "bg": room1_bg,
        "has_lala": True,
        "lala_pos": (200, 150),
        "lala_lives": 3,
        "has_scorpion": False,
        "scorpion_pos": (600, 420),
        "scorpion_lives": 5,
    },
    {
        "bg": room2_bg,
        "has_lala": True,
        "lala_pos": (500, 500),
        "lala_lives": 3,
        "has_scorpion": False,
        "scorpion_pos": (600, 600),
        "scorpion_lives": 5,
    },
]

# variables
current_room = 0

speed = 5

lala_lives = 0
lala_alive = False
lala_rect = None

# lulu_lives = 10
# lulu_alive = False
# lulu_rect = lulu_img.get_rect(topleft=(0, 0))

scorpion_active = False
scorpion_lives = 0

player_lives = 10
max_player_lives = 10

knives = []
knife_speed = 10
max_knives = 3

spikes = []
spike_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(spike_img, (150, 100, 255), (7, 7), 7)
spike_speed = 12
max_spikes = 5

poison_spews = []
poison_speed = 6
poison_damage = 1
poison_img = pygame.Surface((12, 12), pygame.SRCALPHA)
pygame.draw.circle(poison_img, (64, 200, 64), (6, 6), 6)

lala_slimes = []
lala_slime_speed = 6
lala_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala_slime_img, (150, 100, 255), (7, 7), 7)
lala_slime_timer = 0
lala_slime_min_cd = 60
lala_slime_max_cd = 180

lulu_slimes = []
lulu_slime_speed = 6
lulu_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lulu_slime_img, (150, 100, 255), (7, 7), 7)
lulu_slime_timer = 0
lulu_slime_min_cd = 60
lulu_slime_max_cd = 180

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
spike_inv_img = pygame.transform.smoothscale(
    spike_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))
wood_inv_img = pygame.transform.smoothscale(
    wood_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))
stone_inv_img = pygame.transform.smoothscale(
    stone_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))
axe_inv_img = pygame.transform.smoothscale(
    axe_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))

# crafting
ITEM_KNIFE = 0
ITEM_CACTUS = 1
ITEM_SPIKE = 2
ITEM_WOOD = 3
ITEM_STONE = 4
ITEM_AXE = 5

item_imgs = [knife_inv_img, food_inv_img, spike_inv_img,
             wood_inv_img, stone_inv_img, axe_inv_img]


for i in range(max(0, 6 - len(item_imgs))):
    empty = pygame.Surface(
        (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)), pygame.SRCALPHA)
    item_imgs.append(empty)

inventory = [None] * INV_SLOTS
equipped_index = 0

dropped_items = [
    {
        'type': ITEM_KNIFE,
        'rect': knife_img.get_rect(topleft=(500, 400)),
        'img': knife_img
    },
    {
        'type': ITEM_WOOD,
        'rect': wood_img.get_rect(topleft=(400, 420)),
        'img': wood_img
    },
    {
        'type': ITEM_STONE,
        'rect': stone_img.get_rect(topleft=(450, 420)),
        'img': stone_img
    },
]

is_crafting_open = False

game_state = "start_screen"
dialogue_index = 0
space_released = True
dialogue_done = False

# MELEE / AXE variables
axe_cooldown_frames = 30  # cooldown between swings
axe_timer = 0
axe_damage = 2
axe_range = 100  # horizontal range of the swing
axe_height = 80  # vertical size of the swing hitbox

# functions


def reset_game_state():
    global current_room, lala_lives, lala_alive, lala_rect, player_lives
    global knives, player_rect, facing, player_invulnerable, invulnerable_timer
    global equipped_index, inventory, dropped_items, game_state, dialogue_index, space_released, dialogue_done
    global scorpion_active, scorpion_rect, poison_spews, scorpion_lives, lala_slimes, lala_slime_timer, spikes
    global is_crafting_open, axe_timer
    current_room = 0
    room = rooms[current_room]
    lala_lives = room.get("lala_lives", 0)
    lala_alive = bool(room.get("has_lala", False))
    lala_rect = lala_img.get_rect(topleft=room.get("lala_pos", (0, 0)))
    scorpion_active = bool(room.get("has_scorpion", False))
    scorpion_rect.topleft = room.get("scorpion_pos", (0, 0))
    scorpion_lives = room.get("scorpion_lives", 0)
    poison_spews = []
    lala_slimes = []
    lala_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    player_lives = max_player_lives
    knives = []
    spikes = []
    player_rect.bottomleft = (100, 750)
    facing = "right"
    player_invulnerable = False
    invulnerable_timer = 0
    equipped_index = 0
    inventory = [None] * INV_SLOTS
    dropped_items = [
        {
            'type': ITEM_KNIFE,
            'rect': knife_img.get_rect(topleft=(500, 400)),
            'img': knife_img
        },
        {
            'type': ITEM_WOOD,
            'rect': wood_img.get_rect(topleft=(400, 420)),
            'img': wood_img
        },
        {
            'type': ITEM_STONE,
            'rect': stone_img.get_rect(topleft=(450, 420)),
            'img': stone_img
        },
    ]
    game_state = "start_screen"
    dialogue_index = 0
    space_released = True
    dialogue_done = False
    is_crafting_open = False
    axe_timer = 0


reset_game_state()


def enter_room(new_room_index, from_right):
    global current_room, lala_lives, lala_alive, lala_rect, scorpion_active, scorpion_rect, poison_spews, scorpion_lives, lala_slime_timer
    current_room = new_room_index
    room = rooms[current_room]
    lala_lives = room.get("lala_lives", 0)
    lala_alive = bool(room.get("has_lala", False))
    lala_rect.topleft = room.get("lala_pos", (0, 0))
    scorpion_active = bool(room.get("has_scorpion", False))
    scorpion_rect.topleft = room.get("scorpion_pos", (0, 0))
    scorpion_lives = room.get("scorpion_lives", 0)
    poison_spews = []
    lala_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
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
        idx = inventory[i]
        if idx is not None and idx < len(item_imgs):
            item_rect = item_imgs[idx].get_rect()
            item_rect.center = rect.center
            surface.blit(item_imgs[idx], item_rect)


quest_button_x = 1115
quest_button_y = 50

# crafting
def count_item_in_inventory(item_type):
    return sum(1 for it in inventory if it == item_type)


def consume_items_from_inventory(requirements):
    for item_type, need in requirements.items():
        remaining = need
        for i, it in enumerate(inventory):
            if remaining <= 0:
                break
            if it == item_type:
                inventory[i] = None
                remaining -= 1
    return


def find_free_inventory_slot():
    for i, it in enumerate(inventory):
        if it is None:
            return i
    return None

def update_player(mod, counter):
    # mod: defines walking state (player walks left, right, up, down)
    # counter = counts numbers of passed frames/clock ticks in this run cycle (min 0, max 60)

    if counter >= 60:
        counter = 0
    if mod == 0:
        if counter < 30:
            act = 2
        if counter >= 30 and counter < 60:
            act = 3
    if mod == 1:
        if counter < 30:
            act = 0
        if counter >= 30 and counter < 60:
            act = 1
    if mod == 2:
        if counter < 30:
            act = 4
        if counter >= 30 and counter < 60:
            act = 5
    if mod == 3:
        if counter < 30:
            act = 6
        if counter >= 30 and counter < 60:
            act = 7
    count += 1

    return act, counter

#crafting,axe
def craft_axe():
    req = {ITEM_WOOD: 1, ITEM_STONE: 1}
    for item_type, need in req.items():
        if count_item_in_inventory(item_type) < need:
            return False
    consume_items_from_inventory(req)
    free = find_free_inventory_slot()
    if free is not None:
        inventory[free] = ITEM_AXE
    else:
        px = player_rect.centerx + 20
        py = player_rect.centery
        rect = axe_img.get_rect(topleft=(px, py))
        dropped_items.append({'type': ITEM_AXE, 'rect': rect, 'img': axe_img})
    return True

# crafting, display
def display_crafting_panel(surface):
    panel_w, panel_h = 360, 160
    panel_x, panel_y = 20, height - panel_h - 20
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    pygame.draw.rect(surface, (60, 60, 60), panel_rect)
    pygame.draw.rect(surface, (200, 200, 200), panel_rect, 3)

    title = instr_font.render("Crafting (C to toggle)", True, (240, 240, 240))
    surface.blit(title, (panel_x + 10, panel_y + 8))

    recipe_text = font.render("Axe: Wood + Stone", True, (220, 220, 220))
    surface.blit(recipe_text, (panel_x + 10, panel_y + 40))

    wood_count = count_item_in_inventory(ITEM_WOOD)
    stone_count = count_item_in_inventory(ITEM_STONE)
    wc = font.render(f"Wood: {wood_count}", True, (220, 220, 220))
    sc = font.render(f"Stone: {stone_count}", True, (220, 220, 220))
    surface.blit(wc, (panel_x + 10, panel_y + 70))
    surface.blit(sc, (panel_x + 10, panel_y + 95))

    craftable = (wood_count >= 1 and stone_count >= 1)
    btn_w, btn_h = 120, 36
    btn_x, btn_y = panel_x + panel_w - btn_w - 12, panel_y + panel_h - btn_h - 12
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    pygame.draw.rect(surface, (100, 180, 100)
                     if craftable else (90, 90, 90), btn_rect)
    btn_text = font.render("Craft Axe", True, (10, 10, 10))
    surface.blit(btn_text, (btn_x + (btn_w - btn_text.get_width()) // 2,
                            btn_y + (btn_h - btn_text.get_height()) // 2))
    return btn_rect


# main game loop
while run:
    mouse_pos = pygame.mouse.get_pos()
    mouse = mouse_pos
    keys = pygame.key.get_pressed()

    screen.blit(rooms[current_room]["bg"], (0, 0))
    screen.blit(quest_button, (quest_button_x, quest_button_y))

    active_player_frame_index, count = update_player(
        player_mode, active_player_frame_index)

   # reihenfolge (game states)
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if quest_button_x <= mouse[0] <= quest_button_x + 125 and quest_button_y <= mouse[1] <= quest_button_y + 75:
            is_quest_box_shown = not is_quest_box_shown
    if game_state == "start_screen":
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            game_state = "intro"
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
                if inventory[equipped_index] == ITEM_KNIFE:
                    k_rect = knife_img.get_rect(center=player_rect.center)
                    vx = knife_speed if facing == "right" else -knife_speed
                    if vx > 0:
                        k_rect.left = player_rect.right
                    else:
                        k_rect.right = player_rect.left
                    knives.append({'rect': k_rect, 'vx': vx})
            if event.key == pygame.K_t and len(spikes) < max_spikes:
                if inventory[equipped_index] == ITEM_SPIKE:
                    s_rect = spike_img.get_rect(center=player_rect.center)
                    vx = spike_speed if facing == "right" else -spike_speed
                    if vx > 0:
                        s_rect.left = player_rect.right
                    else:
                        s_rect.right = player_rect.left
                    spikes.append({'rect': s_rect, 'vx': vx})
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
                    py = player_rect.bottom - \
                        item_imgs[drop_item].get_height()
                    if drop_item < len(item_imgs):
                        dr_img = item_imgs[drop_item]
                    else:
                        dr_img = knife_img
                    rect = dr_img.get_rect(topleft=(px, py))
                    dropped_items.append({
                        'type': drop_item,
                        'rect': rect,
                        'img': dr_img if isinstance(dr_img, pygame.Surface) else knife_img
                    })
                    inventory[equipped_index] = None
            if event.key == pygame.K_f and inventory[equipped_index] == ITEM_CACTUS:
                player_lives = min(player_lives + 1, max_player_lives)
                inventory[equipped_index] = None
            if lala_lives == 1:
                game_state = "postfight_dialogue"
                dialogue_index = 0

            if event.key == pygame.K_c:
                is_crafting_open = not is_crafting_open

            # AXE melee attack: press X to swing when axe is equipped
            if event.key == pygame.K_x:
                if inventory[equipped_index] == ITEM_AXE and axe_timer <= 0:
                    # create swing hitbox based on facing
                    if facing == "right":
                        swing_rect = pygame.Rect(
                            player_rect.right, player_rect.centery - axe_height // 2, axe_range, axe_height)
                    else:
                        swing_rect = pygame.Rect(
                            player_rect.left - axe_range, player_rect.centery - axe_height // 2, axe_range, axe_height)
                    # hit lala
                    if lala_alive and swing_rect.colliderect(lala_rect):
                        lala_lives = max(0, lala_lives - axe_damage)
                        if lala_lives <= 0:
                            lala_alive = False
                    # hit scorpion
                    if scorpion_active and swing_rect.colliderect(scorpion_rect):
                        scorpion_lives = max(
                            0, scorpion_lives - axe_damage)
                        if scorpion_lives <= 0:
                            scorpion_active = False
                    # set cooldown
                    axe_timer = axe_cooldown_frames

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_crafting_open:
                btn_rect = display_crafting_panel(screen)
                if btn_rect.collidepoint(event.pos):
                    if craft_axe():
                        pass

        # reset player image/facing mode
        if event.type == pygame.KEYUP:
            player_mode = 0

    elif game_state == "postfight_dialogue":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_released:
            dialogue_index += 1
            space_released = False
            if dialogue_index >= len(postfight_dialogue):
                game_state = "main"
                dialogue_done = True
                scorpion_active = True
                scorpion_rect.topleft = rooms[current_room].get(
                    "scorpion_pos", scorpion_rect.topleft)
                scorpion_lives = rooms[current_room].get(
                    "scorpion_lives", scorpion_lives)
                has_cactus = any(item.get('type') ==
                                 ITEM_CACTUS for item in dropped_items)
                if not has_cactus:
                    cx = scorpion_rect.left
                    cy = scorpion_rect.bottom + 10
                    rect = cactusfruit_img.get_rect(topleft=(cx, cy))
                    dropped_items.append({
                        'type': ITEM_CACTUS,
                        'rect': rect,
                        'img': cactusfruit_img
                    })
                lala_slime_timer = random.randint(
                    lala_slime_min_cd, lala_slime_max_cd)
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space_released = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            rects = get_inventory_rects()
            for i, rect in enumerate(rects):
                if rect.collidepoint(event.pos):
                    equipped_index = i

# game states
if game_state == "start_screen":
    screen.fill((172, 147, 98))
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

if game_state == "intro":
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

    if scorpion_active:
        if random.random() < 0.01:
            sx, sy = scorpion_rect.center
            px, py = player_rect.center
            dx = px - sx
            dy = py - sy
            dist = (dx*dx + dy*dy) ** 0.5
            if dist == 0:
                dist = 1
            vx = (dx / dist) * poison_speed
            vy = (dy / dist) * poison_speed
            p = {
                'x': sx - poison_img.get_width() / 2,
                'y': sy - poison_img.get_height() / 2,
                'vx': vx,
                'vy': vy,
                'rect': poison_img.get_rect(center=(int(sx), int(sy)))
            }
            poison_spews.append(p)

# knife mechanics
    for k in knives[:]:
        k['rect'].x += k['vx']
        if k['rect'].right < 0 or k['rect'].left > width:
            knives.remove(k)
            continue
        if lala_alive and k['rect'].colliderect(lala_rect):
            lala_lives = max(0, lala_lives - 1)
            knives.remove(k)
            continue
        if scorpion_active and k['rect'].colliderect(scorpion_rect):
            scorpion_lives = max(0, scorpion_lives - 1)
            knives.remove(k)
            if scorpion_lives <= 0:
                scorpion_active = False
            continue

# spike mechanics
    for s in spikes[:]:
        s['rect'].x += s['vx']
        if s['rect'].right < 0 or s['rect'].left > width:
            spikes.remove(s)
            continue
        if scorpion_active and s['rect'].colliderect(scorpion_rect):
            scorpion_lives = max(0, scorpion_lives - 1)
            spikes.remove(s)
            if scorpion_lives <= 0:
                scorpion_active = False
                continue

# lala attack
    if lala_alive:
        lala_slime_timer -= 1
        if lala_slime_timer <= 0:
            if scorpion_active:
                tx, ty = scorpion_rect.center
                target_flag = 'scorpion'
            else:
                tx, ty = player_rect.center
                target_flag = 'player'
            lx, ly = lala_rect.center
            dx = tx - lx
            dy = ty - ly
            dist = (dx*dx + dy*dy) ** 0.5
            if dist == 0:
                dist = 1
            vx = (dx / dist) * lala_slime_speed
            vy = (dy / dist) * lala_slime_speed
            s = {
                'x': lx - lala_slime_img.get_width() / 2,
                'y': ly - lala_slime_img.get_height() / 2,
                'vx': vx,
                'vy': vy,
                'rect': lala_slime_img.get_rect(center=(int(lx), int(ly))),
                'target': target_flag,
                'age': 0  # age in frames -> used to scale damage over time
            }
            lala_slimes.append(s)
            lala_slime_timer = random.randint(
                lala_slime_min_cd, lala_slime_max_cd)

# lala attack, colliding
    for l in lala_slimes[:]:
        l['x'] += l['vx']
        l['y'] += l['vy']
        l['age'] += 1  # increase age each frame
        l['rect'].topleft = (int(l['x']), int(l['y']))
        if l['rect'].right < 0 or l['rect'].left > width or l['rect'].bottom < 0 or l['rect'].top > height:
            try:
                lala_slimes.remove(l)
            except ValueError:
                pass
            continue
        if l.get('target') == 'scorpion' and scorpion_active and l['rect'].colliderect(scorpion_rect):
            scorpion_lives = max(0, scorpion_lives - 1)
            try:
                lala_slimes.remove(l)
            except ValueError:
                pass
            if scorpion_lives <= 0:
                scorpion_active = False
            continue
        if l.get('target') == 'player' and l['rect'].colliderect(player_rect):
            if not player_invulnerable:
                # Damage scales with age: base 1, +1 every 120 frames (approx every 2 seconds at 60fps), capped at 5
                damage = 1 + (l.get('age', 0) // 120)
                damage = min(damage, 5)
                player_lives = max(0, player_lives - damage)
                player_invulnerable = True
                invulnerable_timer = invulnerable_frames
            try:
                lala_slimes.remove(l)
            except ValueError:
                pass
            continue

# lulu attack (commented out because lulu is not active yet)
    # if lulu_alive:
    #     lulu_slime_timer -= 1
    #     if lulu_slime_timer <= 0:
    #         tx, ty = player_rect.center
    #         target_flag = 'player'
    #         lx, ly = lulu_rect.center
    #         dx = tx - lx
    #         dy = ty - ly
    #         dist = (dx*dx + dy*dy) ** 0.5
    #         if dist == 0:
    #             dist = 1
    #         vx = (dx / dist) * lulu_slime_speed
    #         vy = (dy / dist) * lulu_slime_speed
    #         s = {
    #             'x': lx - lulu_slime_img.get_width() / 2,
    #             'y': ly - lulu_slime_img.get_height() / 2,
    #             'vx': vx,
    #             'vy': vy,
    #             'rect': lulu_slime_img.get_rect(center=(int(lx), int(ly))),
    #             'target': target_flag
    #         }
    #         lulu_slimes.append(s)
    #         lulu_slime_timer = random.randint(
    #             lulu_slime_min_cd, lulu_slime_max_cd)

# lulu attack, colliding
    for g in lulu_slimes[:]:
        g['x'] += g['vx']
        g['y'] += g['vy']
        g['rect'].topleft = (int(g['x']), int(g['y']))
        if g['rect'].right < 0 or g['rect'].left > width or g['rect'].bottom < 0 or g['rect'].top > height:
            try:
                lulu_slimes.remove(g)
            except ValueError:
                pass
            continue
        if g.get('target') == 'lala' and lala_alive and g['rect'].colliderect(lala_rect):
            lala_lives = max(0, lala_lives - 1)
            try:
                lulu_slimes.remove(g)
            except ValueError:
                pass
            if lala_lives <= 0:
                lala_alive = False
            continue
        if g.get('target') == 'player' and g['rect'].colliderect(player_rect):
            if not player_invulnerable:
                player_lives = max(0, player_lives - 1)
                player_invulnerable = True
                invulnerable_timer = invulnerable_frames
            try:
                lulu_slimes.remove(g)
            except ValueError:
                pass
            continue

# scorpion attack, colliding
    for p in poison_spews[:]:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['rect'].topleft = (int(p['x']), int(p['y']))
        if p['rect'].right < 0 or p['rect'].left > width or p['rect'].bottom < 0 or p['rect'].top > height:
            poison_spews.remove(p)
            continue
        if p['rect'].colliderect(player_rect):
            if not player_invulnerable:
                player_lives = max(0, player_lives - poison_damage)
                player_invulnerable = True
                invulnerable_timer = invulnerable_frames
            try:
                poison_spews.remove(p)
            except ValueError:
                pass
            continue

# fight mechanics
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

    # decrement axe cooldown timer each main frame
    if axe_timer > 0:
        axe_timer -= 1

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

    for s in spikes:
        screen.blit(spike_img, s['rect'])

    for l in lala_slimes:
        screen.blit(lala_slime_img, l['rect'])

    for g in lulu_slimes:
        screen.blit(lulu_slime_img, g['rect'])

    for p in poison_spews:
        screen.blit(poison_img, p['rect'])

    if scorpion_active:
        screen.blit(scorpion_img, scorpion_rect)
        bar_w = scorpion_img.get_width()
        bar_h = 6
        bar_x = scorpion_rect.left
        bar_y = scorpion_rect.top - bar_h - 4
        if bar_w > 0:
            health_ratio = scorpion_lives / \
                float(rooms[current_room].get(
                    "scorpion_lives", max(1, scorpion_lives)))
            pygame.draw.rect(screen, (120, 120, 120),
                             (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(screen, (200, 50, 50), (bar_x,
                             bar_y, int(bar_w * health_ratio), bar_h))

    if player_invulnerable and (invulnerable_timer // 6) % 2 == 0:
        pass
    else:
        screen.blit(player, player_rect)

    heart_w = heart_img.get_width()
    spacing = 5
    for i in range(player_lives):
        x = 10 + i * (heart_w + spacing)
        y = 10
        screen.blit(heart_img, (x, y))

    pygame.mouse.set_visible(True)
    render_inventory(screen, mouse_pos, equipped_index)

    for item in dropped_items:
        screen.blit(item['img'], item['rect'])

    # crafting UI
    craft_button_rect = None
    if is_crafting_open:
        craft_button_rect = display_crafting_panel(screen)

if game_state == "main":
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += speed
        facing = "right"
        player_mode = 3
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= speed
        facing = "left"
        player_mode = 2
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 220:
        player_rect.y -= speed
        player_mode = 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += speed
        player_mode = 1
    if event.type == pygame.KEYUP:
        player_mode = 0

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
