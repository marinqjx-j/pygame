import pygame
import sys
import time
import random
import math
pygame.init()

class MoveDirection:
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4

width = 1250
height = 770
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

# ensure correct enum name
move_direction = MoveDirection.MOVE_DOWN

player_image_name = "player.front.1.png"
player = pygame.image.load("play.png").convert_alpha()
player = pygame.transform.smoothscale(player, (200, 320))
player_rect = player.get_rect(bottomleft=(100, 750))

# @TODO: obige Zeile muss verschoben werden!
# Sie muss im game loop aufgerufen werden.
# Beispiel:
#    player_image_name, count = update_player(
#        move_direction, active_player_frame_index)
# player = pygame.image.load(player_image_name).convert_alpha()

clock = pygame.time.Clock()
active_player_frame_index = 0
count = 0

# questbox
def display_quest_box(surface):
    quest_rect = pygame.Rect(100, 100, 1050, 570)
    # quest text
    font = pygame.font.SysFont('Times New Roman', 20)
    quest_text = "- go to your friends room\n- grab the knife"

    quest_text_render = font.render(quest_text, True, (172, 147, 98))

    quest_text_x = 150
    quest_text_y = 150

    pygame.draw.rect(surface, (246, 194, 86), quest_rect)
    surface.blit(quest_text_render, (quest_text_x, quest_text_y))

# dialogue (setup)
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
    # options
    # 1. Let them help you.
    # 2. Don't trust them.
]
text_renders = [font.render(text, True, (172, 147, 98))
                for text in first_dialogue]

# images
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

island_bg = pygame.image.load("island.png").convert_alpha()
island_bg = pygame.transform.smoothscale(island_bg, (width, height))

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

pawbert_img = pygame.image.load("pawbert.png").convert_alpha()
pawbert_rect = pawbert_img.get_rect(bottomleft=(100, 750))

heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (50, 50))

cactusfruit_img = pygame.image.load("cactusfruit.png").convert_alpha()
slot_img = pygame.image.load("slot.png").convert_alpha()
quest_button = pygame.image.load("quest_button.png").convert_alpha()

wood_img = pygame.image.load("wood.png").convert_alpha()
stone_img = pygame.image.load("stone.png").convert_alpha()
scorpion_img = pygame.image.load("scorpion.png").convert_alpha()
scorpion_rect = scorpion_img.get_rect(bottomleft=(100, 750))
axe_img = pygame.image.load("axe.png").convert_alpha()

resin_img = pygame.image.load("resin.png").convert_alpha()
tree_img = pygame.image.load("tree.png").convert_alpha()

is_quest_box_shown = False

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
    },
    {
        "bg": island_bg,
        "has_lala": True,
        "lala_pos": (500, 500),
        "lala_lives": 5,
        "has_scorpion": False
    }
]

# variables
current_room = 0
speed = 5

lala_lives = 0
lala_alive = False
lala_rect = None

scorpion_active = False
scorpion_lives = 0

player_lives = 10
max_player_lives = 10

pawbert_active = False
pawbert_lives = 30
max_pawbert_lives = 30

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

lala1_slimes = []
lala1_slime_speed = 6
lala1_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala1_slime_img, (150, 100, 255), (7, 7), 7)
lala1_slime_timer = 0
lala1_slime_min_cd = 60
lala1_slime_max_cd = 180

lala2_slimes = []
lala2_slime_speed = 6
lala2_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala2_slime_img, (150, 100, 255), (7, 7), 7)
lala2_slime_timer = 0
lala2_slime_min_cd = 60
lala2_slime_max_cd = 180

lala3_slimes = []
lala3_slime_speed = 6
lala3_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala3_slime_img, (150, 100, 255), (7, 7), 7)
lala3_slime_timer = 0
lala3_slime_min_cd = 60
lala3_slime_max_cd = 180

lala4_slimes = []
lala4_slime_speed = 6
lala4_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala4_slime_img, (150, 100, 255), (7, 7), 7)
lala4_slime_timer = 0
lala4_slime_min_cd = 60
lala4_slime_max_cd = 180

lala5_slimes = []
lala5_slime_speed = 6
lala5_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala5_slime_img, (150, 100, 255), (7, 7), 7)
lala5_slime_timer = 0
lala5_slime_min_cd = 60
lala5_slime_max_cd = 180

lala6_slimes = []
lala6_slime_speed = 6
lala6_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala6_slime_img, (150, 100, 255), (7, 7), 7)
lala6_slime_timer = 0
lala6_slime_min_cd = 60
lala6_slime_max_cd = 180

lala7_slimes = []
lala7_slime_speed = 6
lala7_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala7_slime_img, (150, 100, 255), (7, 7), 7)
lala7_slime_timer = 0
lala7_slime_min_cd = 60
lala7_slime_max_cd = 180

lala8_slimes = []
lala8_slime_speed = 6
lala8_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala8_slime_img, (150, 100, 255), (7, 7), 7)
lala8_slime_timer = 0
lala8_slime_min_cd = 60
lala8_slime_max_cd = 180

lala9_slimes = []
lala9_slime_speed = 6
lala9_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala9_slime_img, (150, 100, 255), (7, 7), 7)
lala9_slime_timer = 0
lala9_slime_min_cd = 60
lala9_slime_max_cd = 180

lala10_slimes = []
lala10_slime_speed = 6
lala10_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala10_slime_img, (150, 100, 255), (7, 7), 7)
lala10_slime_timer = 0
lala10_slime_min_cd = 60
lala10_slime_max_cd = 180

player_invulnerable = False
invulnerable_frames = 60
invulnerable_timer = 0
facing = "right"

run = True

# inventory (setup)
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

# crafting (setup)
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
# ensure resin index
if len(item_imgs) <= ITEM_RESIN:
    item_imgs.append(resin_inv_img)
else:
    item_imgs[ITEM_RESIN] = resin_inv_img

for i in range(max(0, 9 - len(item_imgs))):
    empty = pygame.Surface(
        (int(SLOT_SIZE*0.6), int(SLOT_SIZE*0.6)), pygame.SRCALPHA)
    item_imgs.append(empty)

# inventory entries are either None or {'type': ITEM_..., 'count': n}
inventory = [None] * INV_SLOTS
equipped_index = 0

# dropped items
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

# MELEE / AXE variables
axe_cooldown_frames = 60
axe_timer = 0
axe_damage = 2
axe_range = 100  # horizontal range of the swing
axe_height = 80  # vertical size of the swing (hitbox)

# enchantment
axe_enchanted = False
AXE_ENCHANT_BONUS = 2  # extra damage
axe_enchant_timer = 0
AXE_ENCHANT_DURATION = 60 * 30

first_fight_done = False
scorpion_ever_active = False

# inventory functions
def count_item_in_inventory(item_type):
    return sum(slot['count'] for slot in inventory if slot is not None and slot['type'] == item_type)

def add_item_to_inventory(item_type, amount=1):
    """
    Try to add 'amount' of item_type to inventory.
    Returns leftover amount that could not be added (0 if fully added).
    """
    remaining = amount
    # first stack into existing stacks
    for slot in inventory:
        if remaining <= 0:
            break
        if slot is not None and slot['type'] == item_type and slot['count'] < MAX_STACK:
            can_add = min(MAX_STACK - slot['count'], remaining)
            slot['count'] += can_add
            remaining -= can_add
    # then fill new slots
    for i, slot in enumerate(inventory):
        if remaining <= 0:
            break
        if slot is None:
            put = min(MAX_STACK, remaining)
            inventory[i] = {'type': item_type, 'count': put}
            remaining -= put
    return remaining

def consume_items_from_inventory(requirements):
    """
    requirements: dict[item_type] = needed_count
    Removes items from inventory according to requirements.
    Assumes there are enough items. Returns None.
    """
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
    return

def find_free_inventory_slot():
    for i, it in enumerate(inventory):
        if it is None:
            return i
    return None

def get_slot_type(idx):
    s = inventory[idx]
    return None if s is None else s['type']

def remove_one_from_slot(idx):
    """
    Remove one unit from slot idx. If count becomes zero, clear slot.
    """
    if inventory[idx] is None:
        return False
    inventory[idx]['count'] -= 1
    if inventory[idx]['count'] <= 0:
        inventory[idx] = None
    return True

# functions
def update_player(move_direction, counter):
    # move_direction: defines walking state (player walks left, right, up, down)
    # counter = counts numbers of passed frames/clock ticks in this run cycle (min 0, max 60)

    # default
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

# crafting functions
def craft_axe():
    req = {ITEM_WOOD: 1, ITEM_STONE: 1}
    for item_type, need in req.items():
        if count_item_in_inventory(item_type) < need:
            return False
    consume_items_from_inventory(req)
    leftover = add_item_to_inventory(ITEM_AXE, 1)
    if leftover > 0:
        # drop the axe near player if inventory full
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

    # Raft crafting, require 4 wood, 3 resin
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

# initialize/reset trees per room and other state
def create_trees_for_room(room_index):
    """
    Create tree objects for the room using room['trees'] positions.
    Requires tree_img to be not None.
    """
    tlist = []
    if tree_img is None:
        return tlist
    room = rooms[room_index]
    for pos in room.get("trees", []):
        tr = tree_img.copy()
        rect = tr.get_rect(topleft=pos)
        tlist.append({'rect': rect, 'health': 3, 'img': tr})
    return tlist


# main reset
def reset_game_state():
    global current_room, lala_lives, lala_alive, lala_rect, player_lives
    global knives, player_rect, facing, player_invulnerable, invulnerable_timer
    global equipped_index, inventory, dropped_items, game_state, dialogue_index, space_released, dialogue_done
    global scorpion_active, scorpion_rect, poison_spews, scorpion_lives, lala_slimes, lala_slime_timer, spikes
    global is_crafting_open, axe_timer, trees, first_fight_done, scorpion_ever_active, raft_objects
    global axe_enchanted, axe_enchant_timer, poisoned_from_lala, lala_poison_timer, lala_poison_tick_timer
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
    # trees are NOT created at the start; only after the first fight (if tree_img exists)
    trees = []
    first_fight_done = False
    scorpion_ever_active = False
    game_state = "start_screen"
    dialogue_index = 0
    space_released = True
    dialogue_done = False
    is_crafting_open = False
    axe_timer = 0
    # raft objects present in world (deployed)
    raft_objects = []
    # enchant reset
    axe_enchanted = False
    axe_enchant_timer = 0
    poisoned_from_lala = False
    lala_poison_timer = 0
    lala_poison_tick_timer = 0


reset_game_state()

# raft crafting mini-game variables
raft_crafting = False
raft_palette = []  # list of dicts: {'used': False, 'rect': Rect}
# list of dicts: {'rect': Rect, 'angle': int, 'snapped': bool}
placed_planks = []
selected_plank = None
PLANK_SIZE = (140, 48)  # width, height
plank_img = pygame.transform.smoothscale(wood_img, PLANK_SIZE)

# raft assembly area and snap grid settings
RAFT_AREA_W = 600
RAFT_AREA_H = 280
SNAP_COLS = 6
SNAP_ROWS = 3
SNAP_GAP_X = 100
SNAP_GAP_Y = 80
SNAP_THRESHOLD = 28  # pixels to snap
MIN_PLANKS_TO_TIE = 4
RESIN_NEEDED_TO_TIE = 3

# drowning / water variables
breath_max = 180  # frames of breath in water (~3s at 60fps)
player_breath = breath_max
in_water = False
prev_in_water = False  # track previous frame (for crossing detection)
# raft objects in world
raft_objects = []  # list of dicts: {'rect': Rect}


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
    # create palette rects bottom-left area
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
    # require at least MIN_PLANKS_TO_TIE planks
    if len(planks) < MIN_PLANKS_TO_TIE:
        return False
    # build adjacency by distance threshold (centers)
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
    # BFS from 0
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
    # Need resin
    if count_item_in_inventory(ITEM_RESIN) < RESIN_NEEDED_TO_TIE:
        return False
    if not check_raft_connected(placed_planks):
        return False
    needed_wood = len(placed_planks)
    # consume wood and resin
    consume_items_from_inventory(
        {ITEM_WOOD: needed_wood, ITEM_RESIN: RESIN_NEEDED_TO_TIE})
    leftover = add_item_to_inventory(ITEM_RAFT, 1)
    if leftover > 0:
        # drop raft near player
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
    # return wood from palette back to inventory (they were never removed from inventory until tied)
    raft_crafting = False
    raft_palette = []
    placed_planks = []


def deploy_raft_at_player():
    """
    Remove a raft from inventory and place it in the world at player's position.
    """
    # find raft in inventory
    for i, slot in enumerate(inventory):
        if slot is not None and slot['type'] == ITEM_RAFT:
            # use one
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
    # only create trees if first fight already happened and tree_img exists
    if first_fight_done and tree_img is not None:
        trees = create_trees_for_room(current_room)
    else:
        trees = []
    if from_right:
        player_rect.right = width
    else:
        player_rect.left = 0
    # reset water crossing tracker so we don't accidentally trigger enchant on immediate enter
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
                # fallback
                item_surf = item_imgs[0]
            item_rect = item_surf.get_rect()
            item_rect.center = rect.center
            surface.blit(item_surf, item_rect)
            if cnt > 1:
                # render count
                cnt_surf = font.render(str(cnt), True, (240, 240, 240))
                surface.blit(cnt_surf, (rect.right - cnt_surf.get_width() -
                             6, rect.bottom - cnt_surf.get_height() - 4))


quest_button_x = 1115
quest_button_y = 50

# main game loop
while run:
    mouse_pos = pygame.mouse.get_pos()
    mouse = mouse_pos
    keys = pygame.key.get_pressed()

    screen.blit(rooms[current_room]["bg"], (0, 0))
    screen.blit(quest_button, (quest_button_x, quest_button_y))

    # remember previous in_water state to detect crossing from water -> land
    prev_in_water = in_water

    player_image_name, active_player_frame_index = update_player(
        move_direction, active_player_frame_index)

    # check water collision for current room
    water_rects = []
    for w in rooms[current_room].get("water", []):
        water_rects.append(pygame.Rect(w))

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
                        else:
                            # couldn't pick fully, leave it
                            pass
                if event.key == pygame.K_g:
                    slot = inventory[equipped_index]
                    if slot is not None:
                        drop_type = slot['type']
                        # decrease one unit
                        remove_one_from_slot(equipped_index)
                        # choose image for drop
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
                        # consume one cactus
                        remove_one_from_slot(equipped_index)
                        player_lives = min(player_lives + 1, max_player_lives)
                if lala_lives == 1:
                    game_state = "postfight_dialogue"
                    dialogue_index = 0

                if event.key == pygame.K_c:
                    is_crafting_open = not is_crafting_open

                # AXE melee attack: press X to swing when axe is equipped
                if event.key == pygame.K_x:
                    if get_slot_type(equipped_index) == ITEM_AXE and axe_timer <= 0:
                        # effective damage takes enchant into account
                        eff_damage = axe_damage + (AXE_ENCHANT_BONUS if axe_enchanted else 0)
                        # create swing hitbox based on facing
                        if facing == "right":
                            swing_rect = pygame.Rect(
                                player_rect.right, player_rect.centery - axe_height // 2, axe_range, axe_height)
                        else:
                            swing_rect = pygame.Rect(
                                player_rect.left - axe_range, player_rect.centery - axe_height // 2, axe_range, axe_height)
                        # hit lala
                        if lala_alive and swing_rect.colliderect(lala_rect):
                            lala_lives = max(0, lala_lives - eff_damage)
                            if lala_lives <= 0:
                                lala_alive = False
                        # hit scorpion
                        if scorpion_active and swing_rect.colliderect(scorpion_rect):
                            scorpion_lives = max(
                                0, scorpion_lives - eff_damage)
                            if scorpion_lives <= 0:
                                scorpion_active = False
                        # set cooldown
                        axe_timer = axe_cooldown_frames

                # deploy raft if 'R' pressed
                if event.key == pygame.K_r:
                    deployed = deploy_raft_at_player()
                    # nothing else needed; raft appears in world

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # first check crafting button if open
                    if is_crafting_open:
                        btn_rect, raft_rect = display_crafting_panel(screen)
                        if btn_rect.collidepoint(event.pos):
                            if craft_axe():
                                pass
                        if raft_rect.collidepoint(event.pos):
                            # start raft crafting mini-game
                            start_raft_crafting()
                    # then check clicking trees to chop (left click)
                    else:
                        # iterate trees and see if clicked
                        for t in trees[:]:
                            if t['rect'].collidepoint(event.pos):
                                # must have axe equipped
                                if get_slot_type(equipped_index) == ITEM_AXE:
                                    # must be in range (distance)
                                    px, py = player_rect.center
                                    tx, ty = t['rect'].center
                                    dist = math.hypot(px - tx, py - ty)
                                    CHOP_RANGE = 140
                                    if dist <= CHOP_RANGE:
                                        t['health'] -= 1
                                        # small feedback could be added (sound/anim)
                                        if t['health'] <= 0:
                                            trees.remove(t)
                                            # produce wood items (1-3 pieces per tree)
                                            wood_amount = random.randint(1, 3)
                                            leftover = add_item_to_inventory(
                                                ITEM_WOOD, wood_amount)
                                            if leftover > 0:
                                                # spawn leftover as dropped items
                                                for _ in range(leftover):
                                                    rx = t['rect'].left + \
                                                        random.randint(-10, 10)
                                                    ry = t['rect'].bottom
                                                    rect = wood_img.get_rect(
                                                        topleft=(rx, ry))
                                                    dropped_items.append(
                                                        {'type': ITEM_WOOD, 'rect': rect, 'img': wood_img})
                                    else:
                                        # optional: player too far to chop
                                        pass
                                else:
                                    # optional: show message "need an axe"
                                    pass

            # reset player image/facing mode
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

        elif game_state == "scorpion_fight":
            screen.blit(desert_bg, (0, 0))
            if scorpion_active:
                screen.blit(scorpion_img, scorpion_rect)
                bar_w = scorpion_img.get_width()
                bar_h = 6
                bar_x = scorpion_rect.left
                bar_y = scorpion_rect.top - bar_h - 4
                if bar_w > 0:
                    health_ratio = scorpion_lives / float(rooms[current_room].get("scorpion_lives", max(1, scorpion_lives)))
                    pygame.draw.rect(screen, (120, 120, 120), (bar_x, bar_y, bar_w, bar_h))
                    pygame.draw.rect(screen, (200, 50, 50), (bar_x, bar_y, int(bar_w * health_ratio), bar_h))
        
            screen.blit(player, player_rect)
        
            for p in poison_spews:
                screen.blit(poison_img, p['rect'])
    
            for k in knives:
                screen.blit(knife_img, k['rect'])
            for s in spikes:
                screen.blit(spike_img, s['rect'])

        elif game_state == "forest":
            screen.blit(forest_bg, (0, 0))
            screen.blit(player, player_rect)

            for t in trees:
                if t.get('img') is not None:
                    screen.blit(t['img'], t['rect'])
        
            for k in knives:
                screen.blit(knife_img, k['rect'])
        
            # woodcounter
            wood_count = count_item_in_inventory(ITEM_WOOD)
            wood_text = font.render(f"Holz: {wood_count}/8", True, (255, 255, 255))
            screen.blit(wood_text, (10, 50))
        
            if wood_count >= 8:
                msg = font.render("You have enough materials! Go to the shore (right)", True, (100, 200, 100))
                screen.blit(msg, (width // 2 - msg.get_width() // 2, 50))
        
            # lives
            for i in range(player_lives):
                x = 10 + i * (heart_img.get_width() + 5)
                y = height - 70
                screen.blit(heart_img, (x, y))

        #elif game_state == "lalu_dialogue":


        elif game_state == "raft_building":
            screen.blit(island_bg, (0, 0))
        
            pygame.draw.rect(screen, (40, 100, 200), pygame.Rect(0, 600, width, height - 600))
    
            screen.blit(player, player_rect)
            for item in dropped_items:
                screen.blit(item['img'], item['rect'])
        
            # raft menu
            if not raft_crafting:
                msg = font.render("Click R to build a raft", True, (255, 255, 255))
                screen.blit(msg, (width // 2 - msg.get_width() // 2, 100))
            
                wood_count = count_item_in_inventory(ITEM_WOOD)
                resin_count = count_item_in_inventory(ITEM_RESIN)
                wood_text = font.render(f"Holz: {wood_count}/4", True, (200, 200, 200))
                resin_text = font.render(f"Harz: {resin_count}/3", True, (200, 200, 200))
                screen.blit(wood_text, (width // 2 - 100, 150))
                screen.blit(resin_text, (width // 2 - 100, 180))
            
                if wood_count >= 4 and resin_count >= 3:
                    ready_msg = font.render("Floß gebaut! Drücke SPACE um zu starten", True, (100, 200, 100))
                    screen.blit(ready_msg, (width // 2 - ready_msg.get_width() // 2, 220))
        
            # lives
            for i in range(player_lives):
                x = 10 + i * (heart_img.get_width() + 5)
                y = 10
                screen.blit(heart_img, (x, y))
        
            render_inventory(screen, mouse_pos, equipped_index)
            continue

        elif game_state == "boss_fight":
            screen.blit(island_bg, (0, 0))
            pawbert_active = True
        
            pygame.draw.rect(screen, (40, 100, 200), pygame.Rect(0, 600, width, height - 600))
        
            screen.blit(player, player_rect)
            if pawbert_active:
                screen.blit(pawbert_img, pawbert_rect)
        
            for k in knives:
                screen.blit(knife_img, k['rect'])
        
            for p in poison_spews:
                screen.blit(poison_img, p['rect'])
        
            if pawbert_active:
                bar_w = 200
                bar_h = 20
                bar_x = (width - bar_w) // 2
                bar_y = 50
                pygame.draw.rect(screen, (120, 120, 120), (bar_x, bar_y, bar_w, bar_h))
                health_ratio = pawbert_lives / float(max_pawbert_lives)
                pygame.draw.rect(screen, (200, 50, 50), (bar_x, bar_y, int(bar_w * health_ratio), bar_h))
    
        
            #if pawbert_lives <= 0:
        
            for i in range(player_lives):
                x = 10 + i * (heart_img.get_width() + 5)
                y = 10
                screen.blit(heart_img, (x, y))
        
            render_inventory(screen, mouse_pos, equipped_index)
            pygame.display.update()
            clock.tick(60)
            continue

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
                # click on palette to pick a plank (if click inside palette area region)
                picked = None
                for p in raft_palette:
                    if not p['used'] and p['rect'].collidepoint(pos):
                        picked = p
                        break
                if picked is not None:
                    # place a new plank centered at mouse
                    r = plank_img.get_rect(center=pos)
                    placed_planks.append(
                        {'rect': r, 'angle': 0, 'snapped': False})
                    picked['used'] = True
                    selected_plank = placed_planks[-1]
                else:
                    # check snap cells or select plank
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
                    # if near snap cell, snap visually (but keep selected until mouse up)
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
                    # try to tie (requires resin)
                    success = finish_raft_crafting()
                    # on failure, nothing happens; player can rearrange
                if event.key == pygame.K_ESCAPE:
                    cancel_raft_crafting()

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
                vx = (dx / dist) * lala_slime_speed
                vy = (dy / dist) * lala_slime_speed
                s = {
                    'x': lx - lala_slime_img.get_width() / 2,
                    'y': ly - lala_slime_img.get_height() / 2,
                    'vx': vx,
                    'vy': vy,
                    'rect': lala_slime_img.get_rect(center=(int(lx), int(ly))),
                    'target': target_flag,
                    'age': 0 
                }
                lala_slimes.append(s)
                lala_slime_timer = random.randint(lala_slime_min_cd, lala_slime_max_cd)

    # lala attack, colliding
        for l in lala_slimes[:]:
            l['x'] += l['vx']
            l['y'] += l['vy']
            l['age'] += 1  
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

    # lulu attack, colliding (commented out because lulu is not active yet)
        #for g in lulu_slimes[:]:
            #g['x'] += g['vx']
            #g['y'] += g['vy']
            #g['rect'].topleft = (int(g['x']), int(g['y']))
            #if g['rect'].right < 0 or g['rect'].left > width or g['rect'].bottom < 0 or g['rect'].top > height:
                #try:
                    #lulu_slimes.remove(g)
                #except ValueError:
                    #pass
                #continue
            #if g.get('target') == 'lala' and lala_alive and g['rect'].colliderect(lala_rect):
                #lala_lives = max(0, lala_lives - 1)
                #try:
                    #lulu_slimes.remove(g)
                #except ValueError:
                    #pass
                #if lala_lives <= 0:
                    #lala_alive = False
                #continue
            #if g.get('target') == 'player' and g['rect'].colliderect(player_rect):
                #if not player_invulnerable:
                    #player_lives = max(0, player_lives - 1)
                    #player_invulnerable = True
                    #invulnerable_timer = invulnerable_frames
                #try:
                    #lulu_slimes.remove(g)
                #except ValueError:
                    #pass
                #continue

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

        if axe_timer > 0:
            axe_timer -= 1

        # handle axe enchant timer
        if axe_enchanted and axe_enchant_timer > 0:
            axe_enchant_timer -= 1
            if axe_enchant_timer <= 0:
                axe_enchanted = False

        if scorpion_ever_active and (not scorpion_active) and (not first_fight_done):
            first_fight_done = True
            if tree_img is not None:
                trees = create_trees_for_room(current_room)

        if player_lives <= 0:
            reset_game_state()
            continue

        in_water = any(player_rect.colliderect(w) for w in water_rects)
        if prev_in_water and (not in_water):
            #if rooms[current_room].get("has_lala", False) and lala_alive:
            # enchanting
            def display_enchanting_panel(surface):
                paneltwo_w, paneltwo_h = 700, 400
                paneltwo_x, paneltwo_y = 100, height - panel_h - 100
                paneltwo_rect = pygame.Rect(paneltwo_x, paneltwo_y, paneltwo_w, paneltwo_h)
                pygame.draw.rect(surface, (300, 300, 300), paneltwo_rect)
                pygame.draw.rect(surface, (500, 500, 500), paneltwo_rect, 3)

                itle = instr_font.render("Enchanting (O to toggle)", True, (250, 250, 250))
                surface.blit(title, (paneltwo_x + 20, paneltwo_y + 16))

                enchant_text = font.render("Enchant Axe: Axe + LaLa's poison", True, (230, 230, 230))
                surface.blit(enchant_text, (paneltwo_x + 20, paneltwo_y + 60))
 
                axe_count = count_item_in_inventory(ITEM_AXE)
                poison_count = count_item_in_inventory(ITEM_POISON)
                ac = font.render(f"Axe: {axe_count}", True, (230, 230, 230))
                pc = font.render(f"Poison: {poison_count}", True, (230, 230, 230))
                surface.blit(ac, (paneltwo_x + 20, paneltwo_y + 140))
                surface.blit(pc, (paneltwo_x + 20, paneltwo_y + 180))

                able_to_enchant = axe_count >= 1 and poison_count >= 1
                btntwo_w, btntwo_h = 120, 36
                btntwo_x, btntwo_y = paneltwo_x + paneltwo_w - btntwo_w - 12, paneltwo_y + panel_h - btntwo_h - 12
                btn_rect = pygame.Rect(btntwo_x, btntwo_y, btntwo_w, btntwo_h)
                pygame.draw.rect(surface, (100, 180, 100)
                if able_to_enchant
                    #axe_enchanted = True
                    #axe_enchant_timer = AXE_ENCHANT_DURATION
                    else (90, 90, 90), btn_rect)
                btn_text = font.render("Enchant Axe", True, (10, 10, 10))
                surface.blit(btn_text, (btntwo_x + (btntwo_w - btn_text.get_width()) // 2,
                btntwo_y + (btntwo_h - btn_text.get_height()) // 2))


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

        # raft movement
        player_on_raft = False
        for r in raft_objects:
            if player_rect.colliderect(r['rect']):
                player_on_raft = True
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    r['rect'].x += speed
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    r['rect'].x -= speed
                # limit raft to screen
                r['rect'].x = max(0, min(width - r['rect'].width, r['rect'].x))

        # water detection (drowning)
        if in_water and not player_on_raft:
            player_breath -= 1
            if player_breath <= 0:
                player_lives = 0
            # breath bar
            bar_w = 160
            bar_h = 10
            bx = (width - bar_w) // 2
            by = 50
            pygame.draw.rect(screen, (40, 40, 40), (bx, by, bar_w, bar_h))
            breath_ratio = max(0, player_breath) / float(breath_max)
            pygame.draw.rect(screen, (50, 150, 230),
                             (bx, by, int(bar_w * breath_ratio), bar_h))
        else:
            # restore breath
            player_breath = min(player_breath + 2, breath_max)

        if player_invulnerable and (invulnerable_timer // 6) % 2 == 0:
            pass
        else:
            screen.blit(player, player_rect)

        # show enchant/poison HUD
        if axe_enchanted:
            ench_time_s = max(0, axe_enchant_timer // 60)
            ench_surf = instr_font.render(f"Axe enchanted (+{AXE_ENCHANT_BONUS} dmg) {ench_time_s}s", True, (200, 180, 40))
            screen.blit(ench_surf, (10, height - 100))
        if poisoned_from_lala:
            p_time_s = max(0, lala_poison_timer // 60)
            poison_surf = font.render(f"Poisoned by LaLa: {p_time_s}s", True, (180, 40, 40))
            screen.blit(poison_surf, (10, height - 130))

        #life bar
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
        raft_button_rect = None
        if is_crafting_open:
            craft_button_rect, raft_button_rect = display_crafting_panel(
                screen)

    # movement
    if game_state == "main":
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed
            facing = "right"
            move_direction = MoveDirection.MOVE_RIGHT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed
            facing = "left"
            move_direction = MoveDirection.MOVE_LEFT
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.y > 220:
            player_rect.y -= speed
            move_direction = MoveDirection.MOVE_UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed
            move_direction = MoveDirection.MOVE_DOWN


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
        display_quest_box(screen)
        pygame.display.update()
        clock.tick(60)

    # raft crafting rendering (if active, draw overlay and palette)
    if raft_crafting:
        # dim background
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        # drawing area
        area = get_raft_area_rect()
        area_w, area_h = area.width, area.height
        area_x, area_y = area.x, area.y
        pygame.draw.rect(screen, (200, 200, 180),
                         (area_x, area_y, area_w, area_h))
        pygame.draw.rect(screen, (100, 100, 100),
                         (area_x, area_y, area_w, area_h), 3)
        # title and instructions
        title = title_font.render("Raft Assembly", True, (10, 10, 10))
        screen.blit(title, (area_x + 12, area_y + 8))
        instr = font.render(
            "Drag planks from the palette and arrange them into a connected raft. Q/E rotate. Press T to tie (needs 3 resin). Esc to cancel.", True, (10, 10, 10))
        screen.blit(instr, (area_x + 12, area_y + 70))
        # draw placed planks (rotated)
        for pl in placed_planks:
            img = pygame.transform.rotate(plank_img, pl.get('angle', 0))
            img_rect = img.get_rect(center=pl['rect'].center)
            # if it's currently selected, draw highlight
            if pl is selected_plank:
                # semi-opaque preview when moving
                temp = img.copy()
                temp.set_alpha(220)
                screen.blit(temp, img_rect)
                pygame.draw.rect(screen, (30, 160, 30), img_rect, 2)
            else:
                screen.blit(img, img_rect)
                pygame.draw.rect(screen, (80, 50, 20), img_rect, 2)
        # draw palette
        pal_text = font.render("Palette:", True, (10, 10, 10))
        screen.blit(pal_text, (40, height - 230))
        for p in raft_palette:
            # show plank image clipped to palette rect
            img_rect = plank_img.get_rect(center=p['rect'].center)
            screen.blit(plank_img, img_rect)
            if p['used']:
                pygame.draw.rect(screen, (120, 120, 120), p['rect'], 3)
            else:
                pygame.draw.rect(screen, (30, 160, 30), p['rect'], 3)
        # draw snap grid
        for cx, cy in get_snap_cells():
            pygame.draw.circle(screen, (150, 150, 150),
                               (int(cx), int(cy)), 6, 1)
        # draw tie button
        tie_rect = pygame.Rect(area_x + area_w - 140,
                               area_y + area_h - 60, 120, 40)
        pygame.draw.rect(screen, (100, 180, 100), tie_rect)
        tie_text = font.render("Tie (T)", True, (10, 10, 10))
        screen.blit(tie_text, (tie_rect.x + 20, tie_rect.y + 10))
        # cancel button
        cancel_rect = pygame.Rect(
            area_x + area_w - 300, area_y + area_h - 60, 120, 40)
        pygame.draw.rect(screen, (180, 100, 100), cancel_rect)
        cancel_text = font.render("Cancel (Esc)", True, (10, 10, 10))
        screen.blit(cancel_text, (cancel_rect.x + 6, cancel_rect.y + 10))
        pygame.display.update()
        clock.tick(60)
        continue

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
