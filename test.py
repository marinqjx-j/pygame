    from move_directions_enum import MoveDirection
import pygame
import sys
import time
import random
import math
pygame.init()

width = 1250
height = 770
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

move_direction = MoveDirection.MOVE_DOWN

player_image_name = "player.front.1.png"
player = pygame.image.load("play.png").convert_alpha()
player = pygame.transform.smoothscale(player, (200, 320))
player_rect = player.get_rect(bottomleft=(100, 750))

clock = pygame.time.Clock()
active_player_frame_index = 0
count = 0

# ===== QUEST BOX =====
def display_quest_box(surface):
    quest_rect = pygame.Rect(100, 100, 1020, 570)
    font = pygame.font.SysFont('Times New Roman', 20)
    quest_text = "- go to your friends room\n- grab the knife"
    quest_text_render = font.render(quest_text, True, (255, 69, 0))
    quest_text_x = 150
    quest_text_y = 150
    pygame.draw.rect(surface, (246, 194, 86), quest_rect)
    surface.blit(quest_text_render, (quest_text_x, quest_text_y))

# ===== KEY GUIDE =====
def display_key_guide(surface):
    keys_rect = pygame.Rect(100, 205, 1020, 465)
    font = pygame.font.SysFont('Times New Roman', 20)
    keys_texts = ["W A S D or Arrow Keys => movement",
                  "e => pick up", "f => eat"]
    keys_text_renders = [font.render(text, True, (72, 72, 72))
                         for text in keys_texts]
    keys_text_x = 150
    keys_text_y = 250
    pygame.draw.rect(surface, (200, 195, 189), keys_rect)
    for renderer in keys_text_renders:
        surface.blit(renderer, (keys_text_x, keys_text_y))
        keys_text_y += 40

# ===== DIALOGUE SETUP =====
font = pygame.font.SysFont('Times New Roman', 20)
player_header = ["You"]
lala_header = ["LaLa"]
first_dialogue = [
    "Where's my friend?"
    "I know where he is."
    "What are you?!"
]
postfight_dialogue = [
    "I'm a LaLa and I'm trying to help you. Let me explain first."
    "Why do you even know him? And what even is a LaLa?"
    "I know, what happened to your friend. I used to work for this guy [...]"
    "Well, Mr. Labufi wants all the LaLas in the world to work for him. And your friend, he knows their locations. I don't know where he is, can you help me find him and save the LaL[...]"
]
lulu_dialogue = [
    "A human just told me that Mr. Pawbert actually harms other people."
    "A human told you that? They've hurt us in the past, we can't believe them."
    "But there was another LaLa with him and they're friends."
    "So, how exactly does Mr. Pawbert harm people?"
    "He kidnapped the human's friend to help invade the region."
    "Let us see this human."
]
player_dialogue = [
    "So ... your friend was kidnapped by Mr. Pawbert?"
    "Yeah, that's what happened."
    "Fine, we'll help you. Let's free your friend together."
]
text_renders = [font.render(text, True, (172, 147, 98))
                for text in first_dialogue]

# ===== IMAGES =====
room1_bg = pygame.image.load("raum_von_player.png").convert_alpha()
room1_bg = pygame.transform.smoothscale(room1_bg, (width, height))

room2_bg = pygame.image.load("raum_von_players_freund.png").convert_alpha()
room2_bg = pygame.transform.smoothscale(room2_bg, (width, height))

kitchen_bg = pygame.image.load("kitchen.png").convert_alpha()
kitchen_bg = pygame.transform.smoothscale(kitchen_bg, (width, height))

desert_bg = pygame.image.load("desert_background.png").convert_alpha()
desert_bg = pygame.transform.smoothscale(desert_bg, (width, height))

forest_bg = pygame.image.load("forest_background.png").convert_alpha()
forest_bg = pygame.transform.smoothscale(forest_bg, (width, height))

lala_img = pygame.image.load("lala.png").convert_alpha()
lulu_img = pygame.image.load("lulu.png").convert_alpha()

lala1_img = pygame.image.load("lulu.png").convert_alpha()
lala2_img = pygame.image.load("lulu.png").convert_alpha()
lala3_img = pygame.image.load("lulu.png").convert_alpha()
lala4_img = pygame.image.load("lulu.png").convert_alpha()
lala5_img = pygame.image.load("lulu.png").convert_alpha()
lala6_img = pygame.image.load("lulu.png").convert_alpha()
lala7_img = pygame.image.load("lulu.png").convert_alpha()
lala8_img = pygame.image.load("lulu.png").convert_alpha()
lala9_img = pygame.image.load("lulu.png").convert_alpha()
lala10_img = pygame.image.load("lulu.png").convert_alpha()

panel_img = pygame.image.load("panel.png").convert_alpha()
panel_img = pygame.transform.smoothscale(panel_img, (800, 250))

knife_img = pygame.image.load("knife.png").convert_alpha()
spike_img = pygame.image.load("spike.png").convert_alpha()

heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (50, 50))

cactusfruit_img = pygame.image.load("cactusfruit.png").convert_alpha()
slot_img = pygame.image.load("slot.png").convert_alpha()
quest_button = pygame.image.load("quest_button.png").convert_alpha()
keys_button = pygame.image.load("keys_button.png").convert_alpha()

wood_img = pygame.image.load("wood.png").convert_alpha()
stone_img = pygame.image.load("stone.png").convert_alpha()
scorpion_img = pygame.image.load("scorpion.png").convert_alpha()
scorpion_rect = scorpion_img.get_rect(bottomleft=(100, 750))
axe_img = pygame.image.load("axe.png").convert_alpha()

resin_img = pygame.image.load("resin.png").convert_alpha()
tree_img = pygame.image.load("tree.png").convert_alpha()

is_quest_box_shown = False
is_keys_guide_shown = False

rooms = [
    {
        "bg": room1_bg,
        "has_lala": False,
        "lala_pos": (800, 500),
        "lala_lives": 3,
        "has_scorpion": False,
        "scorpion_pos": (600, 420),
        "scorpion_lives": 5,
    },
    {
        "bg": room2_bg,
        "has_lala": False,
        "has_scorpion": False,
    },
    {
        "bg": kitchen_bg,
        "has_lala": True,
        "lala_pos": (500, 500),
        "lala_lives": 3,
        "has_scorpion": False,
        "scorpion_pos": (600, 600),
        "scorpion_lives": 5,
    },
    {
        "bg": desert_bg,
        "has_lala": True,
        "lala_pos": (500, 500),
        "lala_lives": 3,
        "has_scorpion": True,
        "scorpion_pos": (600, 600),
        "scorpion_lives": 5,
    },
    {
        "bg": forest_bg,
        "has_lala": True,
        "lala_pos": (500, 500),
        "lala_lives": 3,
        "has_scorpion": False,
        "trees": [(300, 420), (520, 420)],
        "water": [(0, 650, 1250, 120)],
    }
]

# ===== GAME VARIABLES =====
current_room = 0
speed = 5

lala_lives = 0
lala_alive = False
lala_rect = None

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

# ===== BOSS FIGHT VARIABLES - ALLE 10 LALAS =====
lala1_alive = False
lala1_rect = None
lala1_lives = 3
lala1_slimes = []
lala1_slime_timer = 0

lala2_alive = False
lala2_rect = None
lala2_lives = 3
lala2_slimes = []
lala2_slime_timer = 0

lala3_alive = False
lala3_rect = None
lala3_lives = 3
lala3_slimes = []
lala3_slime_timer = 0

lala4_alive = False
lala4_rect = None
lala4_lives = 3
lala4_slimes = []
lala4_slime_timer = 0

lala5_alive = False
lala5_rect = None
lala5_lives = 3
lala5_slimes = []
lala5_slime_timer = 0

lala6_alive = False
lala6_rect = None
lala6_lives = 3
lala6_slimes = []
lala6_slime_timer = 0

lala7_alive = False
lala7_rect = None
lala7_lives = 3
lala7_slimes = []
lala7_slime_timer = 0

lala8_alive = False
lala8_rect = None
lala8_lives = 3
lala8_slimes = []
lala8_slime_timer = 0

lala9_alive = False
lala9_rect = None
lala9_lives = 3
lala9_slimes = []
lala9_slime_timer = 0

lala10_alive = False
lala10_rect = None
lala10_lives = 3
lala10_slimes = []
lala10_slime_timer = 0

player_invulnerable = False
invulnerable_frames = 60
invulnerable_timer = 0
facing = "right"

run = True

# ===== INVENTORY SETUP =====
title_font = pygame.font.SysFont('Times New Roman', 64)
instr_font = pygame.font.SysFont('Times New Roman', 28)

INV_SLOTS = 5
SLOT_SIZE = 64
SLOT_SPACING = 10
MAX_STACK = 20
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
resin_inv_img = pygame.transform.smoothscale(
    resin_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))

# ===== CRAFTING SETUP =====
ITEM_KNIFE = 0
ITEM_CACTUS = 1
ITEM_SPIKE = 2
ITEM_WOOD = 3
ITEM_STONE = 4
ITEM_AXE = 5
ITEM_RAFT = 6
ITEM_RESIN = 7
ITEM_POISON = 8

item_imgs = [knife_inv_img, food_inv_img, spike_inv_img,
             wood_inv_img, stone_inv_img, axe_inv_img, None, resin_inv_img]

try:
    raft_img = pygame.image.load("raft.png").convert_alpha()
    raft_inv_img = pygame.transform.smoothscale(
        raft_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))
except Exception:
    raft_inv_img = pygame.transform.smoothscale(
        wood_img, (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)))

if len(item_imgs) <= ITEM_RAFT:
    while len(item_imgs) <= ITEM_RAFT:
        item_imgs.append(pygame.Surface(
            (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)), pygame.SRCALPHA))
item_imgs[ITEM_RAFT] = raft_inv_img

if len(item_imgs) <= ITEM_RESIN:
    item_imgs.append(resin_inv_img)
else:
    item_imgs[ITEM_RESIN] = resin_inv_img

for i in range(max(0, 9 - len(item_imgs))):
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
    {
        'type': ITEM_RESIN,
        'rect': resin_img.get_rect(topleft=(470, 370)),
        'img': resin_img
    },
]

is_crafting_open = False
trees = []

game_state = "start_screen"
dialogue_index = 0
space_released = True
dialogue_done = False

# ===== MELEE / AXE VARIABLES =====
axe_cooldown_frames = 60
axe_timer = 0
axe_damage = 2
axe_range = 100
axe_height = 80

axe_enchanted = False
AXE_ENCHANT_BONUS = 2
axe_enchant_timer = 0
AXE_ENCHANT_DURATION = 60 * 30

first_fight_done = False
scorpion_ever_active = False

# ===== INVENTORY FUNCTIONS =====
def count_item_in_inventory(item_type):
    return sum(slot['count'] for slot in inventory if slot is not None and slot['type'] == item_type)

def add_item_to_inventory(item_type, amount=1):
    remaining = amount
    for slot in inventory:
        if remaining <= 0:
            break
        if slot is not None and slot['type'] == item_type and slot['count'] < MAX_STACK:
            can_add = min(MAX_STACK - slot['count'], remaining)
            slot['count'] += can_add
            remaining -= can_add
    for i, slot in enumerate(inventory):
        if remaining <= 0:
            break
        if slot is None:
            put = min(MAX_STACK, remaining)
            inventory[i] = {'type': item_type, 'count': put}
            remaining -= put
    return remaining

def consume_items_from_inventory(requirements):
    for item_type, need in requirements.items():
        remaining = need
        for i, slot in enumerate(inventory):
            if remaining <= 0:
                break
            if slot is not None and slot['type'] == item_type:
                take = min(slot['count'], remaining)
                slot['count'] -= take
                remaining -= take
                if slot['count'] <= 0:
                    inventory[i] = None

def find_free_inventory_slot():
    for i, it in enumerate(inventory):
        if it is None:
            return i
    return None

def get_slot_type(idx):
    s = inventory[idx]
    return None if s is None else s['type']

def remove_one_from_slot(idx):
    if inventory[idx] is None:
        return False
    inventory[idx]['count'] -= 1
    if inventory[idx]['count'] <= 0:
        inventory[idx] = None
    return True

# ===== UPDATE PLAYER =====
def update_player(move_direction, counter):
    img_name = "player.front.1.png"
    GAME_FPS = 60

    if counter >= GAME_FPS:
        counter = 0
    if move_direction == MoveDirection.MOVE_RIGHT:
        if counter < (GAME_FPS/2):
            img_name = "player.right.1.png"
        if counter >= (GAME_FPS/2) and counter < GAME_FPS:
            img_name = "player.right.2.png"
    if move_direction == MoveDirection.MOVE_LEFT:
        if counter < (GAME_FPS/2):
            img_name = "player.left.1.png"
        if counter >= (GAME_FPS/2) and counter < GAME_FPS:
            img_name = "player.left.2.png"
    if move_direction == MoveDirection.MOVE_UP:
        if counter < (GAME_FPS/2):
            img_name = "player.back.1.png"
        if counter >= (GAME_FPS/2) and counter < GAME_FPS:
            img_name = "player.back.2.png"
    if move_direction == MoveDirection.MOVE_DOWN:
        if counter < (GAME_FPS/2):
            img_name = "player.front.1.png"
        if counter >= (GAME_FPS/2) and counter < GAME_FPS:
            img_name = "player.front.2.png"

    global count
    count += 1

    return img_name, counter

# ===== CRAFTING FUNCTIONS =====
def craft_axe():
    req = {ITEM_WOOD: 1, ITEM_STONE: 1}
    for item_type, need in req.items():
        if count_item_in_inventory(item_type) < need:
            return False
    consume_items_from_inventory(req)
    leftover = add_item_to_inventory(ITEM_AXE, 1)
    if leftover > 0:
        px = player_rect.centerx + 20
        py = player_rect.centery
        rect = axe_img.get_rect(topleft=(px, py))
        dropped_items.append({'type': ITEM_AXE, 'rect': rect, 'img': axe_img})
    return True

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
    resin_count = count_item_in_inventory(ITEM_RESIN)
    wc = font.render(f"Wood: {wood_count}", True, (220, 220, 220))
    sc = font.render(f"Stone: {stone_count}", True, (220, 220, 220))
    rc = font.render(f"Resin: {resin_count}", True, (220, 220, 220))
    surface.blit(wc, (panel_x + 10, panel_y + 70))
    surface.blit(sc, (panel_x + 10, panel_y + 95))
    surface.blit(rc, (panel_x + 10, panel_y + 120))

    craftable = (wood_count >= 1 and stone_count >= 1)
    btn_w, btn_h = 120, 36
    btn_x, btn_y = panel_x + panel_w - btn_w - 12, panel_y + panel_h - btn_h - 12
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    pygame.draw.rect(surface, (100, 180, 100)
                     if craftable else (90, 90, 90), btn_rect)
    btn_text = font.render("Craft Axe", True, (10, 10, 10))
    surface.blit(btn_text, (btn_x + (btn_w - btn_text.get_width()) // 2,
                            btn_y + (btn_h - btn_text.get_height()) // 2))

    raft_rect = None
    raft_w = 120
    raft_h = 36
    raft_x = btn_x - raft_w - 8
    raft_y = btn_y
    raft_rect = pygame.Rect(raft_x, raft_y, raft_w, raft_h)
    raft_enabled = (wood_count >= 4)
    pygame.draw.rect(surface, (100, 140, 220)
                     if raft_enabled else (70, 70, 70), raft_rect)
    raft_text = font.render("Make Raft", True, (10, 10, 10))
    surface.blit(raft_text, (raft_x + (raft_w - raft_text.get_width()) // 2,
                             raft_y + (raft_h - raft_text.get_height()) // 2))

    return btn_rect, raft_rect

def create_trees_for_room(room_index):
    tlist = []
    if tree_img is None:
        return tlist
    room = rooms[room_index]
    for pos in room.get("trees", []):
        tr = tree_img.copy()
        rect = tr.get_rect(topleft=pos)
        tlist.append({'rect': rect, 'health': 3, 'img': tr})
    return tlist

# ===== RESET GAME STATE =====
def reset_game_state():
    global current_room, lala_lives, lala_alive, lala_rect, player_lives
    global knives, player_rect, facing, player_invulnerable, invulnerable_timer
    global equipped_index, inventory, dropped_items, game_state, dialogue_index, space_released, dialogue_done
    global scorpion_active, scorpion_rect, poison_spews, scorpion_lives, lala_slimes, lala_slime_timer, spikes
    global is_crafting_open, axe_timer, trees, first_fight_done, scorpion_ever_active, raft_objects
    global axe_enchanted, axe_enchant_timer
    global lala1_alive, lala2_alive, lala3_alive, lala4_alive, lala5_alive
    global lala6_alive, lala7_alive, lala8_alive, lala9_alive, lala10_alive
    global lala1_slimes, lala2_slimes, lala3_slimes, lala4_slimes, lala5_slimes
    global lala6_slimes, lala7_slimes, lala8_slimes, lala9_slimes, lala10_slimes
    
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
        {
            'type': ITEM_RESIN,
            'rect': resin_img.get_rect(topleft=(470, 370)),
            'img': resin_img
        },
    ]
    trees = []
    first_fight_done = False
    scorpion_ever_active = False
    game_state = "start_screen"
    dialogue_index = 0
    space_released = True
    dialogue_done = False
    is_crafting_open = False
    axe_timer = 0
    raft_objects = []
    axe_enchanted = False
    axe_enchant_timer = 0
    
    # Reset alle LaLas
    lala1_alive = False
    lala1_slimes = []
    lala2_alive = False
    lala2_slimes = []
    lala3_alive = False
    lala3_slimes = []
    lala4_alive = False
    lala4_slimes = []
    lala5_alive = False
    lala5_slimes = []
    lala6_alive = False
    lala6_slimes = []
    lala7_alive = False
    lala7_slimes = []
    lala8_alive = False
    lala8_slimes = []
    lala9_alive = False
    lala9_slimes = []
    lala10_alive = False
    lala10_slimes = []

reset_game_state()

# ===== RAFT VARIABLES =====
raft_crafting = False
raft_palette = []
placed_planks = []
selected_plank = None
PLANK_SIZE = (140, 48)
plank_img = pygame.transform.smoothscale(wood_img, PLANK_SIZE)

RAFT_AREA_W = 600
RAFT_AREA_H = 280
SNAP_COLS = 6
SNAP_ROWS = 3
SNAP_GAP_X = 100
SNAP_GAP_Y = 80
SNAP_THRESHOLD = 28
MIN_PLANKS_TO_TIE = 4
RESIN_NEEDED_TO_TIE = 3

breath_max = 180
player_breath = breath_max
in_water = False
prev_in_water = False
raft_objects = []

def start_raft_crafting():
    global raft_crafting, raft_palette, placed_planks, selected_plank
    available = count_item_in_inventory(ITEM_WOOD)
    if available < 4:
        return False
    raft_crafting = True
    raft_palette = []
    placed_planks = []
    selected_plank = None
    palette_count = min(available, 8)
    start_x = 40
    start_y = height - 200
    gap = 12
    for i in range(palette_count):
        r = pygame.Rect(
            start_x + i * (PLANK_SIZE[0] // 2 + gap), start_y, PLANK_SIZE[0], PLANK_SIZE[1])
        raft_palette.append({'used': False, 'rect': r})
    return True

def get_raft_area_rect():
    area_w = RAFT_AREA_W
    area_h = RAFT_AREA_H
    area_x = (width - area_w) // 2
    area_y = (height - area_h) // 2
    return pygame.Rect(area_x, area_y, area_w, area_h)

def get_snap_cells():
    area = get_raft_area_rect()
    cells = []
    start_x = area.x + 40
    start_y = area.y + 80
    for r in range(SNAP_ROWS):
        for c in range(SNAP_COLS):
            cx = start_x + c * SNAP_GAP_X
            cy = start_y + r * SNAP_GAP_Y
            cells.append((cx, cy))
    return cells

def find_nearest_snap(pos):
    cells = get_snap_cells()
    best = None
    best_d = 1e9
    for cx, cy in cells:
        d = math.hypot(pos[0] - cx, pos[1] - cy)
        if d < best_d:
            best_d = d
            best = (cx, cy)
    if best_d <= SNAP_THRESHOLD:
        return best
    return None

def check_raft_connected(planks):
    if len(planks) < MIN_PLANKS_TO_TIE:
        return False
    nodes = [p['rect'].center for p in planks]
    n = len(nodes)
    adj = [[] for _ in range(n)]
    THRESH = 120
    for i in range(n):
        for j in range(i+1, n):
            dx = nodes[i][0] - nodes[j][0]
            dy = nodes[i][1] - nodes[j][1]
            if math.hypot(dx, dy) <= THRESH:
                adj[i].append(j)
                adj[j].append(i)
    visited = [False]*n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)

def finish_raft_crafting():
    global raft_crafting, raft_palette, placed_planks, raft_objects
    if count_item_in_inventory(ITEM_RESIN) < RESIN_NEEDED_TO_TIE:
        return False
    if not check_raft_connected(placed_planks):
        return False
    needed_wood = len(placed_planks)
    consume_items_from_inventory(
        {ITEM_WOOD: needed_wood, ITEM_RESIN: RESIN_NEEDED_TO_TIE})
    leftover = add_item_to_inventory(ITEM_RAFT, 1)
    if leftover > 0:
        px = player_rect.centerx + 20
        py = player_rect.centery
        rect = plank_img.get_rect(topleft=(px, py))
        dropped_items.append(
            {'type': ITEM_RAFT, 'rect': rect, 'img': plank_img})
    raft_crafting = False
    raft_palette = []
    placed_planks = []
    return True

def cancel_raft_crafting():
    global raft_crafting, raft_palette, placed_planks
    raft_crafting = False
    raft_palette = []
    placed_planks = []

def deploy_raft_at_player():
    for i, slot in enumerate(inventory):
        if slot is not None and slot['type'] == ITEM_RAFT:
            remove_one_from_slot(i)
            rx = player_rect.centerx - 60
            ry = player_rect.bottom - 20
            rrect = pygame.Rect(rx, ry, 120, 40)
            raft_objects.append({'rect': rrect})
            return True
    return False

def enter_room(new_room_index, from_right):
    global current_room, lala_lives, lala_alive, lala_rect, scorpion_active, scorpion_rect, poison_spews, scorpion_lives, lala_slime_timer, trees, prev_in_water
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
    if first_fight_done and tree_img is not None:
        trees = create_trees_for_room(current_room)
    else:
        trees = []
    if from_right:
        player_rect.right = width
    else:
        player_rect.left = 0
    prev_in_water = False

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
        slot = inventory[i]
        if slot is not None:
            item_type = slot['type']
            cnt = slot['count']
            if item_type < len(item_imgs):
                item_surf = item_imgs[item_type]
            else:
                item_surf = item_imgs[0]
            item_rect = item_surf.get_rect()
            item_rect.center = rect.center
            surface.blit(item_surf, item_rect)
            if cnt > 1:
                cnt_surf = font.render(str(cnt), True, (240, 240, 240))
                surface.blit(cnt_surf, (rect.right - cnt_surf.get_width() -
                             6, rect.bottom - cnt_surf.get_height() - 4))

# ===== BOSS FIGHT INITIALIZATION FUNCTION =====
def start_boss_fight():
    global game_state
    global lala1_alive, lala2_alive, lala3_alive, lala4_alive, lala5_alive
    global lala6_alive, lala7_alive, lala8_alive, lala9_alive, lala10_alive
    global lala1_rect, lala2_rect, lala3_rect, lala4_rect, lala5_rect
    global lala6_rect, lala7_rect, lala8_rect, lala9_rect, lala10_rect
    global lala1_lives, lala2_lives, lala3_lives, lala4_lives, lala5_lives
    global lala6_lives, lala7_lives, lala8_lives, lala9_lives, lala10_lives
    global lala1_slime_timer, lala2_slime_timer, lala3_slime_timer, lala4_slime_timer, lala5_slime_timer
    global lala6_slime_timer, lala7_slime_timer, lala8_slime_timer, lala9_slime_timer, lala10_slime_timer
    
    game_state = "boss_fight"
    
    # Spawne alle 10 LaLas in einem Kreis
    player_x = player_rect.centerx
    player_y = player_rect.centery
    radius = 250
    
    positions = [
        (player_x + radius * math.cos(i * 2 * math.pi / 10), 
         player_y + radius * math.sin(i * 2 * math.pi / 10))
        for i in range(10)
    ]
    
    # Initialisiere alle LaLas
    lala1_alive = True
    lala1_rect = lala1_img.get_rect(center=positions[0])
    lala1_lives = 3
    lala1_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala2_alive = True
    lala2_rect = lala2_img.get_rect(center=positions[1])
    lala2_lives = 3
    lala2_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala3_alive = True
    lala3_rect = lala3_img.get_rect(center=positions[2])
    lala3_lives = 3
    lala3_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala4_alive = True
    lala4_rect = lala4_img.get_rect(center=positions[3])
    lala4_lives = 3
    lala4_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala5_alive = True
    lala5_rect = lala5_img.get_rect(center=positions[4])
    lala5_lives = 3
    lala5_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala6_alive = True
    lala6_rect = lala6_img.get_rect(center=positions[5])
    lala6_lives = 3
    lala6_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala7_alive = True
    lala7_rect = lala7_img.get_rect(center=positions[6])
    lala7_lives = 3
    lala7_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala8_alive = True
    lala8_rect = lala8_img.get_rect(center=positions[7])
    lala8_lives = 3
    lala8_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala9_alive = True
    lala9_rect = lala9_img.get_rect(center=positions[8])
    lala9_lives = 3
    lala9_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)
    
    lala10_alive = True
    lala10_rect = lala10_img.get_rect(center=positions[9])
    lala10_lives = 3
    lala10_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)

quest_button_x = 1115
quest_button_y = 50

keys_button_x = 1115
keys_button_y = 150

# ===== MAIN GAME LOOP =====
while run:
    mouse_pos = pygame.mouse.get_pos()
    mouse = mouse_pos
    keys = pygame.key.get_pressed()

    screen.blit(rooms[current_room]["bg"], (0, 0))
    screen.blit(quest_button, (quest_button_x, quest_button_y))
    screen.blit(keys_button, (keys_button_x, keys_button_y))

    prev_in_water = in_water

    player_image_name, active_player_frame_index = update_player(
        move_direction, active_player_frame_index)

    water_rects = []
    for w in rooms[current_room].get("water", []):
        water_rects.append(pygame.Rect(w))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if quest_button_x <= mouse[0] <= quest_button_x + 125 and quest_button_y <= mouse[1] <= quest_button_y + 75:
                is_quest_box_shown = not is_quest_box_shown
            if keys_button_x <= mouse[0] <= keys_button_x + 125 and keys_button_y <= mouse[1] <= keys_button_y + 75:
                is_keys_guide_shown = not is_keys_guide_shown
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
                    if get_slot_type(equipped_index) == ITEM_KNIFE:
                        k_rect = knife_img.get_rect(center=player_rect.center)
                        vx = knife_speed if facing == "right" else -knife_speed
                        if vx > 0:
                            k_rect.left = player_rect.right
                        else:
                            k_rect.right = player_rect.left
                        knives.append({'rect': k_rect, 'vx': vx})
                if event.key == pygame.K_t and len(spikes) < max_spikes:
                    if get_slot_type(equipped_index) == ITEM_SPIKE:
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
                        item_type = dropped_items[to_pick]['type']
                        leftover = add_item_to_inventory(item_type, 1)
                        if leftover == 0:
                            dropped_items.pop(to_pick)
                if event.key == pygame.K_g:
                    slot = inventory[equipped_index]
                    if slot is not None:
                        drop_type = slot['type']
                        remove_one_from_slot(equipped_index)
                        if drop_type < len(item_imgs):
                            dr_img = item_imgs[drop_type]
                        else:
                            dr_img = knife_img
                        px = player_rect.centerx - dr_img.get_width()//2
                        py = player_rect.bottom - dr_img.get_height()
                        rect = dr_img.get_rect(topleft=(px, py))
                        dropped_items.append({
                            'type': drop_type,
                            'rect': rect,
                            'img': dr_img if isinstance(dr_img, pygame.Surface) else knife_img
                        })
                if event.key == pygame.K_f:
                    if get_slot_type(equipped_index) == ITEM_CACTUS:
                        remove_one_from_slot(equipped_index)
                        player_lives = min(player_lives + 1, max_player_lives)
                if lala_lives == 1:
                    game_state = "postfight_dialogue"
                    dialogue_index = 0

                if event.key == pygame.K_c:
                    is_crafting_open = not is_crafting_open

                if event.key == pygame.K_x:
                    if get_slot_type(equipped_index) == ITEM_AXE and axe_timer <= 0:
                        eff_damage = axe_damage + \
                            (AXE_ENCHANT_BONUS if axe_enchanted else 0)
                        if facing == "right":
                            swing_rect = pygame.Rect(
                                player_rect.right, player_rect.centery - axe_height // 2, axe_range, axe_height)
                        else:
                            swing_rect = pygame.Rect(
                                player_rect.left - axe_range, player_rect.centery - axe_height // 2, axe_range, axe_height)
                        if lala_alive and swing_rect.colliderect(lala_rect):
                            lala_lives = max(0, lala_lives - eff_damage)
                            if lala_lives <= 0:
                                lala_alive = False
                        if scorpion_active and swing_rect.colliderect(scorpion_rect):
                            scorpion_lives = max(
                                0, scorpion_lives - eff_damage)
                            if scorpion_lives <= 0:
                                scorpion_active = False
                        axe_timer = axe_cooldown_frames

                if event.key == pygame.K_r:
                    deployed = deploy_raft_at_player()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if is_crafting_open:
                        btn_rect, raft_rect = display_crafting_panel(screen)
                        if btn_rect.collidepoint(event.pos):
                            if craft_axe():
                                pass
                        if raft_rect.collidepoint(event.pos):
                            start_raft_crafting()
                    else:
                        for t in trees[:]:
                            if t['rect'].collidepoint(event.pos):
                                if get_slot_type(equipped_index) == ITEM_AXE:
                                    px, py = player_rect.center
                                    tx, ty = t['rect'].center
                                    dist = math.hypot(px - tx, py - ty)
                                    CHOP_RANGE = 140
                                    if dist <= CHOP_RANGE:
                                        t['health'] -= 1
                                        if t['health'] <= 0:
                                            trees.remove(t)
                                            wood_amount = random.randint(1, 3)
                                            leftover = add_item_to_inventory(
                                                ITEM_WOOD, wood_amount)
                                            if leftover > 0:
                                                for _ in range(leftover):
                                                    rx = t['rect'].left + \
                                                        random.randint(-10, 10)
                                                    ry = t['rect'].bottom
                                                    rect = wood_img.get_rect(
                                                        topleft=(rx, ry))
                                                    dropped_items.append(
                                                        {'type': ITEM_WOOD, 'rect': rect, 'img': wood_img})

            if event.type == pygame.KEYUP:
                move_direction = MoveDirection.MOVE_DOWN

        elif game_state == "postfight_dialogue":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space_released:
                dialogue_index += 1
                space_released = False
                wood_img = pygame.image.load("wood.png").convert_alpha()
                stone_img = pygame.image.load("stone.png").convert_alpha()
                if dialogue_index >= len(postfight_dialogue):
                    game_state = "main"
                    dialogue_done = True
                    scorpion_active = True
                    scorpion_ever_active = True
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

        # raft crafting events
        if raft_crafting:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                area = get_raft_area_rect()
                picked = None
                for p in raft_palette:
                    if not p['used'] and p['rect'].collidepoint(pos):
                        picked = p
                        break
                if picked is not None:
                    r = plank_img.get_rect(center=pos)
                    placed_planks.append(
                        {'rect': r, 'angle': 0, 'snapped': False})
                    picked['used'] = True
                    selected_plank = placed_planks[-1]
                else:
                    for pl in reversed(placed_planks):
                        if pl['rect'].collidepoint(pos):
                            selected_plank = pl
                            break
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                selected_plank = None
            if event.type == pygame.MOUSEMOTION:
                if selected_plank is not None:
                    mx, my = event.pos
                    selected_plank['rect'].center = (mx, my)
                    snap = find_nearest_snap((mx, my))
                    if snap is not None:
                        selected_plank['rect'].center = snap
                        selected_plank['snapped'] = True
                    else:
                        selected_plank['snapped'] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if selected_plank is not None:
                        selected_plank['angle'] = (
                            selected_plank.get('angle', 0) - 90) % 360
                if event.key == pygame.K_e:
                    if selected_plank is not None:
                        selected_plank['angle'] = (
                            selected_plank.get('angle', 0) + 90) % 360
                if event.key == pygame.K_t:
                    success = finish_raft_crafting()
                if event.key == pygame.K_ESCAPE:
                    cancel_raft_crafting()

    # ===== GAME STATES =====
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

        for wrect in water_rects:
            pygame.draw.rect(screen, (40, 100, 200), wrect)

        for r in raft_objects:
            pygame.draw.rect(screen, (120, 70, 30), r['rect'])
            screen.blit(plank_img, r['rect'])

        for t in trees:
            if t.get('img') is not None:
                screen.blit(t['img'], t['rect'])

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
                vx = (dx / dist) * lala_slime_
