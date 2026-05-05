import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

# ─────────────────────────────────────────────
#  SOUND EFFECTS
# ─────────────────────────────────────────────
def safe_load_sound(path, volume=1.0):
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(volume)
        return s
    except Exception:
        return None

SFX_HIT_DAMAGE   = safe_load_sound("freesound_community-horror-reveal-shock-44757.mp3", 0.7)
SFX_EAT         = safe_load_sound("freesound_community-eating-chips-81092.mp3", 0.8)
SFX_RAFT_PLACE  = safe_load_sound("soundreality-sound-of-mouse-click-4-478760.mp3", 0.6)
SFX_DEATH_1     = safe_load_sound("phatphrogstudio-defeat-outros-game-sounds-collection-477823.mp3", 0.9)
SFX_DEATH_2     = safe_load_sound("freesound_community-failure-1-89170.mp3", 0.9)
SFX_DEATH_3PLUS = safe_load_sound("freesound_community-defeated-sigh-85637.mp3", 0.9)
SFX_ENEMY_WIN   = safe_load_sound("musheran-win-176035.mp3", 0.8)
SFX_CHOP        = safe_load_sound("freesound_community-knife-throw-1-105221.mp3", 0.7)
SFX_THROW       = safe_load_sound("scratchonix-dart-throw-380649.mp3", 0.7)
SFX_ENCHANT     = safe_load_sound("cartoon-music-soundtrack-arcade-game-achievement-bling-489759.mp3", 0.9)
SFX_SLIME       = safe_load_sound("universfield-slime-impact-352473.mp3", 0.7)
SFX_SCORPION    = safe_load_sound("freesound_community-horror-reveal-shock-44757.mp3", 0.8)
SFX_UI_CLICK    = safe_load_sound("freesound_community-ui-click-43196.mp3", 0.6)

def play_sfx(sfx):
    if sfx:
        sfx.play()

# death counter (persists across resets via module-level var)
_death_count = 0

# ─────────────────────────────────────────────
#  MUSIC / MINI-PLAYER
# ─────────────────────────────────────────────
import os

MUSIC_FILES = [
    f for f in [
        "cyberwave-orchestra-puzzle-game-loop-bright-casual-video-game-music-249201__1_.mp3",
    ]
    if os.path.exists(f)
]

music_state = {
    "track_index": 0,
    "playing": False,
    "volume": 0.5,
    "track_name": "",
}

def music_load_and_play(idx):
    if not MUSIC_FILES:
        return
    idx = idx % len(MUSIC_FILES)
    music_state["track_index"] = idx
    path = MUSIC_FILES[idx]
    music_state["track_name"] = os.path.splitext(os.path.basename(path))[0][:32]
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(music_state["volume"])
    pygame.mixer.music.play(-1)   # loop forever
    music_state["playing"] = True

def music_toggle():
    if not MUSIC_FILES:
        return
    if music_state["playing"]:
        pygame.mixer.music.pause()
        music_state["playing"] = False
    else:
        pygame.mixer.music.unpause()
        music_state["playing"] = True

def music_set_volume(v):
    music_state["volume"] = max(0.0, min(1.0, v))
    pygame.mixer.music.set_volume(music_state["volume"])

# Mini-player geometry
MP_W, MP_H = 260, 54
MP_X = 10
MP_Y_OFFSET = 64   # from bottom

def draw_mini_player(surface, mouse_pos):
    """Draw the music mini-player in the bottom-left corner."""
    mp_y = HEIGHT - MP_Y_OFFSET - MP_H
    # background panel
    panel = pygame.Surface((MP_W, MP_H), pygame.SRCALPHA)
    panel.fill((18, 14, 10, 210))
    surface.blit(panel, (MP_X, mp_y))
    pygame.draw.rect(surface, (100, 80, 40), (MP_X, mp_y, MP_W, MP_H), 1)

    mf = pygame.font.SysFont("Times New Roman", 13)
    sf = pygame.font.SysFont("Times New Roman", 11)

    # Music note icon + track name
    note = mf.render("♪", True, (200, 170, 80))
    surface.blit(note, (MP_X + 6, mp_y + 4))
    name = music_state["track_name"] if MUSIC_FILES else "no music file found"
    nt = sf.render(name, True, (200, 185, 150))
    surface.blit(nt, (MP_X + 22, mp_y + 5))

    # Play/Pause button
    btn_x, btn_y, btn_w, btn_h = MP_X + 6, mp_y + 24, 36, 22
    btn_col = (80, 160, 80) if not music_state["playing"] else (160, 80, 80)
    btn_hover = pygame.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos)
    pygame.draw.rect(surface, (min(btn_col[0]+30,255), min(btn_col[1]+30,255), min(btn_col[2]+30,255)) if btn_hover else btn_col,
                     (btn_x, btn_y, btn_w, btn_h))
    lbl = sf.render("▐▐" if music_state["playing"] else "▶", True, (240, 240, 240))
    surface.blit(lbl, (btn_x + btn_w//2 - lbl.get_width()//2, btn_y + btn_h//2 - lbl.get_height()//2))

    # Volume slider
    vol_x, vol_y = MP_X + 50, mp_y + 29
    vol_w = 120
    vol_label = sf.render("Vol", True, (160, 150, 120))
    surface.blit(vol_label, (vol_x, vol_y - 1))
    bar_x = vol_x + 26
    pygame.draw.rect(surface, (60, 55, 45), (bar_x, vol_y + 4, vol_w, 8))
    fill_w = int(vol_w * music_state["volume"])
    pygame.draw.rect(surface, (180, 150, 60), (bar_x, vol_y + 4, fill_w, 8))
    # knob
    kx = bar_x + fill_w
    pygame.draw.circle(surface, (240, 210, 100), (kx, vol_y + 8), 6)

    # return rects for click detection
    play_rect   = pygame.Rect(btn_x,  btn_y,  btn_w, btn_h)
    slider_rect = pygame.Rect(bar_x,  vol_y,  vol_w, 14)
    return play_rect, slider_rect, (bar_x, vol_y + 4, vol_w, 8)

if MUSIC_FILES:
    music_load_and_play(0)


# ─────────────────────────────────────────────
#  WINDOW
# ─────────────────────────────────────────────
WIDTH, HEIGHT = 1250, 770
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save the Lalas!")
clock = pygame.time.Clock()

# ─────────────────────────────────────────────
#  MOVEMENT DIRECTION ENUM
# ─────────────────────────────────────────────


class MoveDirection:
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4

# ─────────────────────────────────────────────
#  HELPER: safe image load (returns coloured
#  placeholder if file is missing)
# ─────────────────────────────────────────────


def safe_load(path, fallback_size=(64, 64), fallback_color=(200, 100, 200)):
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf


def safe_scale(surf, size):
    return pygame.transform.smoothscale(surf, size)


# ─────────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────────
font = pygame.font.SysFont("Times New Roman", 20)
instr_font = pygame.font.SysFont("Times New Roman", 28)
title_font = pygame.font.SysFont("Times New Roman", 64)
small_font = pygame.font.SysFont("Times New Roman", 16)
italic_font = pygame.font.SysFont("Times New Roman", 20, italic=True)

# ─────────────────────────────────────────────
#  PLAYER ANIMATION FRAMES
# ─────────────────────────────────────────────
FRAME_NAMES = [
    "player.front.1.png", "player.front.2.png",
    "player.back.1.png",  "player.back.2.png",
    "player.left.1.png",  "player.left.2.png",
    "player.right.1.png", "player.right.2.png",
]
player_frames = {}
for fn in FRAME_NAMES:
    img = safe_load(fn, (200, 320), (100, 150, 200))
    player_frames[fn] = safe_scale(img, (200, 320))

move_direction = MoveDirection.MOVE_DOWN
player = player_frames["player.front.1.png"]
player_rect = player.get_rect(bottomleft=(100, 750))
active_player_frame_index = 0


def update_player_anim(direction, counter):
    GAME_FPS = 60
    if counter >= GAME_FPS:
        counter = 0
    half = GAME_FPS // 2
    mapping = {
        MoveDirection.MOVE_RIGHT: ("player.right.1.png", "player.right.2.png"),
        MoveDirection.MOVE_LEFT:  ("player.left.1.png",  "player.left.2.png"),
        MoveDirection.MOVE_UP:    ("player.back.1.png",  "player.back.2.png"),
        MoveDirection.MOVE_DOWN:  ("player.front.1.png", "player.front.2.png"),
    }
    pair = mapping.get(direction, ("player.front.1.png", "player.front.2.png"))
    name = pair[0] if counter < half else pair[1]
    counter += 1
    return name, counter


# ─────────────────────────────────────────────
#  IMAGES
# ─────────────────────────────────────────────
# Backgrounds
room1_bg = safe_scale(safe_load("raum_von_player.png",
                      (WIDTH, HEIGHT), (80, 60, 50)),   (WIDTH, HEIGHT))
room2_bg = safe_scale(safe_load("raum_von_players_freund.png",
                      (WIDTH, HEIGHT), (70, 50, 45)),   (WIDTH, HEIGHT))
kitchen_bg = safe_scale(safe_load("kitchen.png",
                        (WIDTH, HEIGHT), (90, 70, 55)),   (WIDTH, HEIGHT))
meadow_bg = safe_scale(safe_load("meadow_background.jpg",
                       (WIDTH, HEIGHT), (80, 140, 60)),  (WIDTH, HEIGHT))
desert_bg = safe_scale(safe_load("desert_background.png",
                       (WIDTH, HEIGHT), (200, 160, 80)), (WIDTH, HEIGHT))
forest_bg = safe_scale(safe_load("forest_background.png",
                       (WIDTH, HEIGHT), (30, 90, 30)),   (WIDTH, HEIGHT))
shore_bg = safe_scale(safe_load("shore_background.png",
                      (WIDTH, HEIGHT), (60, 120, 180)), (WIDTH, HEIGHT))
bossfight_bg = safe_scale(safe_load("bossfight.png",
                          (WIDTH, HEIGHT), (40, 20, 60)),   (WIDTH, HEIGHT))
running_bg = safe_scale(safe_load(
    "meadow_background.jpg",    (WIDTH, HEIGHT), (100, 160, 80)), (WIDTH, HEIGHT))
start_bg = safe_scale(safe_load(
    "bg.jpg",                   (WIDTH, HEIGHT), (10, 8, 20)),    (WIDTH, HEIGHT))

# Characters
lala_img = safe_load("lala.png",   (80, 100), (150, 80, 200))
lulu_img = safe_load("lulu.png",   (80, 100), (80, 180, 200))
lumi_img = safe_load("lumi.png",   (200, 320), (100, 150, 200))
lala_img = safe_scale(lala_img,  (80, 100))
lulu_img = safe_scale(lulu_img,  (80, 100))
lumi_img = safe_scale(lumi_img,  (200, 320))

# Items
knife_img = safe_load("knife.png",      (40, 40),  (180, 180, 180))
spike_img = safe_load("spike.png",      (30, 30),  (180, 100, 80))
heart_img = safe_scale(
    safe_load("heart.png", (50, 50), (220, 50, 50)), (50, 50))
cactusfruit_img = safe_load("cactusfruit.png", (40, 40),  (80, 200, 80))
wood_img = safe_load("wood.png",       (50, 30),  (140, 80, 40))
stone_img = safe_load("stone.png",      (40, 40),  (130, 130, 130))
axe_img = safe_load("axe.png",        (50, 50),  (160, 100, 50))
resin_img = safe_load("resin.png",      (40, 40),  (200, 150, 50))
krypton_img = safe_load("krypton.png",    (40, 40),  (50, 220, 200))
pawbert_img = safe_scale(
    safe_load("pawbert.jpg", (100, 130), (180, 40, 40)), (100, 130))
scorpion_img = safe_load("scorpion.png",   (80, 60),  (180, 80, 30))
tree_img = safe_load("tree.png",       (100, 160), (40, 120, 40))

# UI
slot_img = safe_load("slot.png",        (64, 64),  (60, 60, 60))
quest_button = safe_load("quest_button.png", (125, 75), (180, 140, 60))
keys_button = safe_load("keys_button.png", (125, 75), (60, 100, 180))
panel_img = safe_load("panel.png",       (800, 250), (50, 40, 30))
panel_img = safe_scale(panel_img, (800, 250))

# ── Map image ───────────────────────────────
map_img_raw = safe_load("map.png", (400, 260), (80, 100, 80))
# We'll scale it at runtime depending on zoom level

# Poison projectile surface (used by scorpion)
poison_img = pygame.Surface((12, 12), pygame.SRCALPHA)
pygame.draw.circle(poison_img, (80, 200, 80), (6, 6), 6)

# Lala slime projectile surface
lala_slime_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(lala_slime_img, (150, 100, 255), (7, 7), 7)

scorpion_rect = scorpion_img.get_rect(bottomleft=(600, 600))

# ─────────────────────────────────────────────
#  INVENTORY CONSTANTS & ITEM IDs
# ─────────────────────────────────────────────
INV_SLOTS = 5
SLOT_SIZE = 64
SLOT_SPACING = 10
MAX_STACK = 20

ITEM_KNIFE = 0
ITEM_CACTUS = 1
ITEM_SPIKE = 2
ITEM_WOOD = 3
ITEM_STONE = 4
ITEM_AXE = 5
ITEM_RAFT = 6
ITEM_RESIN = 7
ITEM_KRYPTON = 9


def make_inv_img(src, size=None):
    s = int(SLOT_SIZE * 0.6)
    sz = size or (s, s)
    return safe_scale(src, sz)


slot_img = safe_scale(slot_img, (SLOT_SIZE, SLOT_SIZE))
knife_inv_img = make_inv_img(knife_img)
food_inv_img = make_inv_img(cactusfruit_img)
spike_inv_img = make_inv_img(spike_img)
wood_inv_img = make_inv_img(wood_img)
stone_inv_img = make_inv_img(stone_img)
axe_inv_img = make_inv_img(axe_img)
resin_inv_img = make_inv_img(resin_img)
krypton_inv_img = make_inv_img(krypton_img)

# item_imgs indexed by ITEM_*  (index 8 = placeholder for poison/unused)
item_imgs = [
    knife_inv_img,    # 0
    food_inv_img,     # 1
    spike_inv_img,    # 2
    wood_inv_img,     # 3
    stone_inv_img,    # 4
    axe_inv_img,      # 5
    wood_inv_img,     # 6 raft (reuse wood look)
    resin_inv_img,    # 7
    stone_inv_img,    # 8 placeholder
    krypton_inv_img,  # 9
]

# ─────────────────────────────────────────────
#  DIALOGUE
# ─────────────────────────────────────────────
# Speaker constants
SP_PLAYER = "You"
SP_LALA = "LaLa (Rocky)"
SP_UNKNOWN = "???"
SP_LULU = "LuLu"
SP_LALAS = "LaLas"
SP_PAWBERT = "Mr. Pawbert"
SP_LUMI = "Lumi"
SP_NARR = ""   # narrator / action line
SKIP = False

# Each dialogue line is (speaker, text)
INTRO_DIALOGUE = [
    (SP_NARR,   "*You wake up.*"),
    (SP_PLAYER, "Lumi? Where are you?"),
    (SP_NARR,   "*No answer. Something feels off. You head to the kitchen.*"),
]

# Kitchen dialogue (replaces old INTRO that was triggered in room 0)
KITCHEN_DIALOGUE = [
    (SP_UNKNOWN, "..."),
    (SP_PLAYER,  "What are you?!"),
    (SP_UNKNOWN, "Wait! Don't attack me!"),
]

POSTFIGHT_DIALOGUE = [
    (SP_UNKNOWN, "I'm trying to help you. Let me explain first."),
    (SP_PLAYER,  "What even are you?!"),
    (SP_UNKNOWN, "We are called LaLas — little creatures with magical abilities. I only know your friend because all of us LaLas work for someone called Mr. Pawbert, and he's the one who captured Lumi."),
    (SP_PLAYER,  "What?! Why?!"),
    (SP_UNKNOWN, "He promised us protection from humans. But I think he just wants to use us. I overheard him talking about plans to invade this island."),
    (SP_PLAYER,  "What does Lumi have to do with this?"),
    (SP_UNKNOWN, "Lumi knows every path on the island. That makes him useful to Mr. Pawbert. Will you help me save the LaLas?"),
    (SP_PLAYER,  "...Who are you exactly?"),
    (SP_LALA,    "I'm Rocky. I live in a cave nearby. So — will you help?"),
]

POSTFIGHT_CHOICES = [
    "I'll help you.",
    "Don't trust him.",
]

LUMI_ROOM_DIALOGUE = [
    (SP_NARR,   "*You enter Lumi's room. The bed is empty.*"),
    (SP_PLAYER, "Lumi...?"),
    (SP_NARR,   "*No sign of them. Something is very wrong.*"),
    (SP_PLAYER, "I need to find out what happened."),
]

RUNNING_DIALOGUE = [
    (SP_LALA,   "So, what's your name?"),
    (SP_PLAYER, "{name}"),          # {name} gets replaced at runtime
    (SP_LALA,   "I'm Rocky, because I live in a cave."),
    (SP_PLAYER, "Where are we going?"),
    (SP_LALA,   "We're crossing the island to get to Mr. Pawbert's base."),
    (SP_PLAYER, "Let's go."),
    (SP_NARR,   "*You and Rocky cross the meadow towards the desert.*"),
]

DESERT_DIALOGUE = [
    (SP_LALA,   "Watch out — scorpions live here. Eat the cactus fruit to regain health."),
    (SP_PLAYER, "Got it. Let's keep moving."),
]

LULU_DIALOGUE_1 = [
    (SP_PLAYER, "Stop fighting! We're just trying to help."),
    (SP_LULU,   "Help? How?"),
    (SP_LALA,   "Mr. Pawbert harms people. We have to free the LaLas from working for him."),
    (SP_LULU,   "What? Who'd he harm?"),
    (SP_LALA,   "He kidnapped {name}'s friend!"),
    (SP_PLAYER, "Can you convince the others to join us?"),
]

LULU_DIALOGUE_2 = [
    (SP_LULU,   "A human told me Mr. Pawbert actually harms people."),
    (SP_LALAS,  "A human told you that? They've hurt us before — we can't trust them."),
    (SP_LULU,   "But another LaLa was with them, and they're friends."),
    (SP_LALAS,  "How exactly does Pawbert harm people?"),
    (SP_LULU,   "He kidnapped the human's friend to invade the region."),
    (SP_LALAS,  "Let us see this human."),
    (SP_LALAS,  "So … your friend was kidnapped by Mr. Pawbert?"),
    (SP_PLAYER, "Yeah … that's what happened."),
    (SP_LULU,   "Fine. We'll help you. Let's free your friend together!"),
]

LULU_CHOICES = [
    "Let them help us.",
    "Don't trust them.",
]

SHORE_DIALOGUE = [
    (SP_LALA,   "We need to cross the water. Build a raft from the wood you collected."),
    (SP_PLAYER, "And if I fall in?"),
    (SP_LALA,   "Don't. You'll drown."),
]

BOSS_DIALOGUE = [
    (SP_PLAYER, "Where's my friend?!"),
    (SP_PAWBERT, "Who are you?"),
    (SP_PLAYER, "It doesn't matter. I just want Lumi and the LaLas freed."),
    (SP_PAWBERT, "You can try — but you'll never succeed."),
    (SP_PLAYER, "So where are you hiding them?"),
    (SP_NARR,   "*About 50 LaLas appear behind Mr. Pawbert.*"),
    (SP_LALA,   "Oh no!"),
    (SP_PAWBERT, "Ready? …… ATTACK!"),
    (SP_LALA,   "We'll handle them. Go get him! Take this — it's Krypton. Enchant your axe!"),
]

FINAL_DIALOGUE = [
    (SP_NARR,   "*After the battle, you enter Mr. Pawbert's house.*"),
    (SP_NARR,   "*Lumi stands by the window and turns around.*"),
    (SP_LUMI,   "{name}? Is that you?"),
    (SP_PLAYER, "I finally found you!"),
    (SP_NARR,   "*Reunion! ⭐ The island is safe.*"),
]

# ─────────────────────────────────────────────
#  ROOM DEFINITIONS
# ─────────────────────────────────────────────
#  game_state that is REQUIRED before you may
#  leave a room to the right.
ROOMS = [
    # 0 - player's room (wake up, no lala yet)
    {
        "bg": room1_bg, "name": "Your Room",
        "has_lala": False, "lala_pos": (800, 500), "lala_lives": 3,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": "room_0_intro_done",
        "intro_state": "intro",
        "items_on_enter": [],
    },
    # 1 - friend's room (always accessible, triggers discover dialogue)
    {
        "bg": room2_bg, "name": "Lumi's Room",
        "has_lala": False, "lala_pos": (0, 0), "lala_lives": 0,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": None,
        "intro_state": "lumi_room_dialogue",
        "items_on_enter": [],
    },
    # 2 - kitchen (LaLa encounter + knife pickup)
    {
        "bg": kitchen_bg, "name": "Kitchen",
        "has_lala": True, "lala_pos": (700, 500), "lala_lives": 3,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": "lala_joined",   # must beat LaLa to leave kitchen
        "intro_state": "kitchen_dialogue",
        "items_on_enter": [
            {"type": ITEM_KNIFE, "pos": (400, 600), "img": knife_img},
        ],
    },
    # 3 - meadow
    {
        "bg": meadow_bg, "name": "Meadow",
        "has_lala": False, "lala_pos": (0, 0), "lala_lives": 0,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": None,
        "intro_state": "running_sequence",
        "items_on_enter": [],
    },
    # 4 - desert
    {
        "bg": desert_bg, "name": "Desert",
        "has_lala": False, "lala_pos": (0, 0), "lala_lives": 0,
        "has_scorpion": True, "scorpion_pos": (700, 580), "scorpion_lives": 5,
        "required_state": "scorpion_dead",
        "intro_state": "desert_dialogue",
        "items_on_enter": [
            {"type": ITEM_CACTUS, "pos": (600, 630), "img": cactusfruit_img},
            {"type": ITEM_SPIKE,  "pos": (900, 620), "img": spike_img},
        ],
    },
    # 5 - forest
    {
        "bg": forest_bg, "name": "Forest",
        "has_lala": True, "lala_pos": (350, 480), "lala_lives": 4,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": "lulu_joined",
        "intro_state": "forest_dialogue",
        "trees": [(280, 380), (550, 380), (850, 380)],
        "items_on_enter": [
            {"type": ITEM_WOOD,  "pos": (180, 640), "img": wood_img},
            {"type": ITEM_STONE, "pos": (400, 650), "img": stone_img},
        ],
    },
    # 6 - shore
    {
        "bg": shore_bg, "name": "Shore",
        "has_lala": False, "lala_pos": (0, 0), "lala_lives": 0,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": "raft_crossed",
        "intro_state": "shore_dialogue",
        "water": [(900, 0, 350, 770)],  # water on RIGHT side
        "items_on_enter": [],
    },
    # 7 - boss island
    {
        "bg": bossfight_bg, "name": "Pawbert's Island",
        "has_lala": False, "lala_pos": (0, 0), "lala_lives": 0,
        "has_scorpion": False, "scorpion_pos": (0, 0), "scorpion_lives": 0,
        "required_state": "victory",
        "intro_state": "boss_dialogue",
        "water": [(0, 0, 200, 770)],  # water strip on LEFT side of boss island
        "items_on_enter": [],
    },
]

# ─────────────────────────────────────────────
#  QUEST LIST  (index = quest number)
# ─────────────────────────────────────────────
QUESTS = [
    "Explore the house",
    "Grab the knife",
    "Fight the intruder",
    "Follow LaLa (Rocky)",
    "Eat a cactus fruit",
    "Defend yourself",
    "Follow Rocky through the forest",
    "Craft an axe",
    "Build a raft",
    "Cross to the other side",
    "Enchant your axe",
    "Save the LaLas!",
    "Find Lumi and win!",
]

# ─────────────────────────────────────────────
#  PROJECTILE / COMBAT CONSTANTS
# ─────────────────────────────────────────────
KNIFE_SPEED = 10
MAX_KNIVES = 3
SPIKE_SPEED = 12
MAX_SPIKES = 5

AXE_COOLDOWN = 60
AXE_DAMAGE = 2
AXE_RANGE = 100
AXE_HEIGHT = 80
AXE_ENCHANT_BONUS = 4
AXE_ENCHANT_DURATION = 60 * 30   # 30 seconds

SLIME_MIN_CD = 60
SLIME_MAX_CD = 180
SLIME_SPEED = 6
SLIME_DMG = 1

POISON_SPEED = 5
POISON_CHANCE = 0.008   # per frame

INVULN_FRAMES = 60

BREATH_MAX = 180

# ─────────────────────────────────────────────
#  RAFT MINI-GAME CONSTANTS
# ─────────────────────────────────────────────
PLANK_SIZE = (140, 48)
RAFT_AREA_W = 600
RAFT_AREA_H = 280
SNAP_COLS = 6
SNAP_ROWS = 3
SNAP_GAP_X = 100
SNAP_GAP_Y = 80
SNAP_THRESHOLD = 28
MIN_PLANKS = 1
RESIN_TO_TIE = 1
WOOD_FOR_RAFT = 4

plank_img = safe_scale(wood_img, PLANK_SIZE)

# ─────────────────────────────────────────────
#  PAWBERT (boss)
# ─────────────────────────────────────────────
PAWBERT_MAX_LIVES = 30
PAWBERT_SPEED = 1.5
PAWBERT_ATCK_CD = 120

# ─────────────────────────────────────────────
#  NOTIFICATION SYSTEM
# ─────────────────────────────────────────────
notifications = []   # list of {"text": str, "timer": int}


def notify(text, duration=180):
    notifications.append({"text": text, "timer": duration})


def draw_notifications(surface):
    y = 80
    for n in notifications[:]:
        surf = instr_font.render(n["text"], True, (255, 220, 80))
        alpha = min(255, n["timer"] * 4)
        surf.set_alpha(alpha)
        surface.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
        y += 36
        n["timer"] -= 1
    notifications[:] = [n for n in notifications if n["timer"] > 0]

# ─────────────────────────────────────────────
#  INVENTORY HELPERS
# ─────────────────────────────────────────────


def count_item(inventory, item_type):
    return sum(s["count"] for s in inventory if s and s["type"] == item_type)


def add_item(inventory, item_type, amount=1):
    remaining = amount
    for slot in inventory:
        if remaining <= 0:
            break
        if slot and slot["type"] == item_type and slot["count"] < MAX_STACK:
            add = min(MAX_STACK - slot["count"], remaining)
            slot["count"] += add
            remaining -= add
    for i, slot in enumerate(inventory):
        if remaining <= 0:
            break
        if slot is None:
            put = min(MAX_STACK, remaining)
            inventory[i] = {"type": item_type, "count": put}
            remaining -= put
    return remaining


def consume_items(inventory, requirements):
    for item_type, need in requirements.items():
        remaining = need
        for i, slot in enumerate(inventory):
            if remaining <= 0:
                break
            if slot and slot["type"] == item_type:
                take = min(slot["count"], remaining)
                slot["count"] -= take
                remaining -= take
                if slot["count"] <= 0:
                    inventory[i] = None


def remove_one(inventory, idx):
    if inventory[idx] is None:
        return False
    inventory[idx]["count"] -= 1
    if inventory[idx]["count"] <= 0:
        inventory[idx] = None
    return True


def get_slot_type(inventory, idx):
    s = inventory[idx]
    return None if s is None else s["type"]


def get_inventory_rects():
    total_w = INV_SLOTS * SLOT_SIZE + (INV_SLOTS - 1) * SLOT_SPACING
    start_x = (WIDTH - total_w) // 2
    y = HEIGHT - SLOT_SIZE - 10
    return [pygame.Rect(start_x + i * (SLOT_SIZE + SLOT_SPACING), y, SLOT_SIZE, SLOT_SIZE)
            for i in range(INV_SLOTS)]


def render_inventory(surface, mouse_pos, inventory, equipped):
    rects = get_inventory_rects()
    for i, rect in enumerate(rects):
        if i == equipped:
            pygame.draw.rect(surface, (255, 220, 0), rect.inflate(6, 6), 4)
        elif rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (100, 200, 255), rect.inflate(4, 4), 4)
        surface.blit(slot_img, rect.topleft)
        slot = inventory[i]
        if slot:
            it = slot["type"]
            img = item_imgs[it] if it < len(item_imgs) else item_imgs[0]
            ir = img.get_rect(center=rect.center)
            surface.blit(img, ir)
            if slot["count"] > 1:
                cs = small_font.render(
                    str(slot["count"]), True, (240, 240, 240))
                surface.blit(cs, (rect.right - cs.get_width() - 4,
                                  rect.bottom - cs.get_height() - 2))

# ─────────────────────────────────────────────
#  CRAFTING
# ─────────────────────────────────────────────


def can_craft_axe(inventory):
    return count_item(inventory, ITEM_WOOD) >= 1 and count_item(inventory, ITEM_STONE) >= 1


def do_craft_axe(inventory, dropped_items):
    if not can_craft_axe(inventory):
        return False
    consume_items(inventory, {ITEM_WOOD: 1, ITEM_STONE: 1})
    leftover = add_item(inventory, ITEM_AXE)
    if leftover:
        dropped_items.append({"type": ITEM_AXE,
                              "rect": axe_img.get_rect(topleft=(player_rect.centerx, player_rect.centery)),
                              "img": axe_img})
    notify("Axe crafted! Use X to swing it.")
    return True


def display_crafting_panel(surface, inventory, axe_enchanted, axe_enchant_timer):
    pw, ph = 420, 200
    px, py = 20, HEIGHT - ph - 20
    pygame.draw.rect(surface, (45, 40, 35), (px, py, pw, ph))
    pygame.draw.rect(surface, (180, 150, 80), (px, py, pw, ph), 2)

    title = instr_font.render("Crafting  [C]", True, (240, 210, 80))
    surface.blit(title, (px + 10, py + 8))

    wc = count_item(inventory, ITEM_WOOD)
    sc = count_item(inventory, ITEM_STONE)
    rc = count_item(inventory, ITEM_RESIN)
    kc = count_item(inventory, ITEM_KRYPTON)

    # Resource counts with icons
    res = [
        (wood_inv_img,    f"x{wc} Wood",    (180, 140, 80)),
        (stone_inv_img,   f"x{sc} Stone",   (200, 200, 200)),
        (resin_inv_img,   f"x{rc} Resin",   (220, 180, 60)),
        (krypton_inv_img, f"x{kc} Krypton", (0, 230, 230)),
    ]
    for i, (img, label, color) in enumerate(res):
        ix = px + 12 + (i % 2) * 190
        iy = py + 46 + (i // 2) * 44
        surface.blit(img, (ix, iy))
        surface.blit(font.render(label, True, color), (ix + 30, iy + 8))

    # Recipe hints
    surface.blit(small_font.render("🪓 Axe = 1 Wood + 1 Stone",
                 True, (255, 200, 80)), (px + 12, py + 140))
    surface.blit(small_font.render("🚣 Raft = 4 Wood + 1 Resin  (T to finish)",
                 True, (100, 200, 255)), (px + 12, py + 158))

    # Enchant status
    if axe_enchanted:
        es = font.render(
            f"Axe ENCHANTED  {axe_enchant_timer // 60}s", True, (0, 255, 200))
        surface.blit(es, (px + 220, py + 128))
    elif kc >= 1 and count_item(inventory, ITEM_AXE) >= 1:
        eh = font.render("O = Enchant Axe (1 Krypton)", True, (0, 200, 200))
        surface.blit(eh, (px + 200, py + 128))

    # Craft Axe button
    can = can_craft_axe(inventory)
    btn_w, btn_h = 130, 38
    bx, by = px + pw - btn_w - 12, py + ph - btn_h - 12
    brc = (100, 180, 100) if can else (80, 80, 80)
    btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
    pygame.draw.rect(surface, brc, btn_rect)
    bt = font.render("Craft Axe", True, (10, 10, 10))
    surface.blit(bt, (bx + (btn_w - bt.get_width()) // 2,
                      by + (btn_h - bt.get_height()) // 2))

    # Raft button
    raft_can = wc >= WOOD_FOR_RAFT
    raft_w = 130
    raft_rect = pygame.Rect(bx - raft_w - 8, by, raft_w, btn_h)
    pygame.draw.rect(surface, (80, 120, 200)
                     if raft_can else (70, 70, 70), raft_rect)
    rt = font.render("Make Raft", True, (10, 10, 10))
    surface.blit(rt, (raft_rect.x + (raft_w - rt.get_width()) // 2,
                      raft_rect.y + (btn_h - rt.get_height()) // 2))

    return btn_rect, raft_rect

# ─────────────────────────────────────────────
#  RAFT MINI-GAME HELPERS
# ─────────────────────────────────────────────


def get_raft_area_rect():
    ax = (WIDTH - RAFT_AREA_W) // 2
    ay = (HEIGHT - RAFT_AREA_H) // 2
    return pygame.Rect(ax, ay, RAFT_AREA_W, RAFT_AREA_H)


def get_snap_cells():
    area = get_raft_area_rect()
    cells = []
    sx, sy = area.x + 40, area.y + 80
    for r in range(SNAP_ROWS):
        for c in range(SNAP_COLS):
            cells.append((sx + c * SNAP_GAP_X, sy + r * SNAP_GAP_Y))
    return cells


def find_nearest_snap(pos):
    best, best_d = None, 1e9
    for cell in get_snap_cells():
        d = math.hypot(pos[0] - cell[0], pos[1] - cell[1])
        if d < best_d:
            best_d, best = d, cell
    return best if best_d <= SNAP_THRESHOLD else None


def check_raft_connected(planks):
    if len(planks) < MIN_PLANKS:
        return True
    nodes = [p["rect"].center for p in planks]
    n = len(nodes)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if math.hypot(nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1]) <= 120:
                adj[i].append(j)
                adj[j].append(i)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)


def start_raft_crafting(inventory):
    available = count_item(inventory, ITEM_WOOD)
    if available < WOOD_FOR_RAFT:
        notify(
            f"Need {WOOD_FOR_RAFT} wood to build a raft! You have {available}.")
        return False, [], [], None
    # Always give exactly WOOD_FOR_RAFT planks to place
    sx, sy, gap = 40, HEIGHT - 200, 12
    palette = [{"used": False,
                "rect": pygame.Rect(sx + i * (PLANK_SIZE[0] // 2 + gap), sy, *PLANK_SIZE)}
               for i in range(WOOD_FOR_RAFT)]
    return True, palette, [], None


def finish_raft(inventory, placed_planks):
    if len(placed_planks) < WOOD_FOR_RAFT:
        notify(
            f"Place all {WOOD_FOR_RAFT} planks first! ({len(placed_planks)}/{WOOD_FOR_RAFT})")
        return False
    if count_item(inventory, ITEM_RESIN) < RESIN_TO_TIE:
        notify(f"Need {RESIN_TO_TIE} resin to tie the raft!")
        return False
    if not check_raft_connected(placed_planks):
        notify("Planks must be connected!")
        return False
    consume_items(inventory, {ITEM_WOOD: len(
        placed_planks), ITEM_RESIN: RESIN_TO_TIE})
    add_item(inventory, ITEM_RAFT)
    notify("Raft built! Press R to deploy it.")
    return True


# ─────────────────────────────────────────────
#  DIALOGUE RENDERING
# ─────────────────────────────────────────────
SPEAKER_COLORS = {
    SP_PLAYER:  (100, 200, 255),
    SP_UNKNOWN: (160, 120, 200),
    SP_LALA:    (180, 130, 255),
    SP_LULU:    (80, 220, 180),
    SP_LALAS:   (80, 220, 180),
    SP_PAWBERT: (255, 80, 80),
    SP_LUMI:    (255, 200, 80),
    SP_NARR:    (180, 180, 180),
}


def render_dialogue_panel(surface, speaker, text, choices=None, selected=0, speaker2=None):
    """Draws the dialogue box at the bottom of the screen."""
    panel_h = 160
    panel_y = HEIGHT - panel_h - 10
    panel_rect = pygame.Rect(20, panel_y, WIDTH - 40, panel_h)
    # background
    overlay = pygame.Surface((panel_rect.w, panel_rect.h), pygame.SRCALPHA)
    overlay.fill((20, 15, 10, 220))
    surface.blit(overlay, panel_rect.topleft)
    pygame.draw.rect(surface, (172, 147, 98), panel_rect, 2)

    # speaker header
    if speaker:
        color = SPEAKER_COLORS.get(speaker, (220, 220, 220))
        sp_surf = instr_font.render(speaker, True, color)
        surface.blit(sp_surf, (panel_rect.x + 16, panel_rect.y + 10))

    # text  (word-wrap)
    words = text.split()
    lines, line = [], ""
    max_w = panel_rect.w - 32
    for w in words:
        test = (line + " " + w).strip()
        if font.size(test)[0] > max_w:
            lines.append(line)
            line = w
        else:
            line = test
    if line:
        lines.append(line)

    ty = panel_rect.y + 44
    text_font = italic_font if speaker == SP_NARR else font
    text_color = (180, 180, 180) if speaker == SP_NARR else (220, 200, 160)
    for l in lines[:3]:
        ts = text_font.render(l, True, text_color)
        surface.blit(ts, (panel_rect.x + 16, ty))
        ty += 24

    # choices — start BELOW the dialogue text
    if choices:
        cy = panel_rect.y + 90   # push below speaker name + text
        for i, ch in enumerate(choices):
            col = (255, 210, 60) if i == selected else (180, 180, 180)
            prefix = "▸ " if i == selected else "  "
            cs = font.render(prefix + ch, True, col)
            surface.blit(cs, (panel_rect.x + 30, cy))
            cy += 32
    else:
        hint = small_font.render("SPACE to continue", True, (120, 110, 90))
        surface.blit(hint, (panel_rect.right - hint.get_width() - 12,
                            panel_rect.bottom - hint.get_height() - 6))

# ─────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────


def draw_hp_bar(surface, x, y, current, maximum, w=200, h=18, color=(200, 50, 50)):
    pygame.draw.rect(surface, (60, 60, 60), (x, y, w, h))
    ratio = max(0, current / max(1, maximum))
    pygame.draw.rect(surface, color, (x, y, int(w * ratio), h))
    pygame.draw.rect(surface, (180, 180, 180), (x, y, w, h), 2)


def draw_hearts(surface, lives, max_lives):
    """Filled hearts = current HP, dimmed hearts = lost HP."""
    hw = heart_img.get_width() + 4
    show = min(max_lives, 10)
    for i in range(show):
        if i < lives:
            surface.blit(heart_img, (10 + i * hw, 10))
        else:
            dark = heart_img.copy()
            dark.set_alpha(55)
            surface.blit(dark, (10 + i * hw, 10))


def draw_quest(surface, quest_index):
    if 0 <= quest_index < len(QUESTS):
        text = f"▸  {QUESTS[quest_index]}"
        qs = font.render(text, True, (255, 220, 80))
        bg = pygame.Surface((qs.get_width() + 16, 26), pygame.SRCALPHA)
        bg.fill((20, 15, 10, 180))
        # Draw bottom-left so it never overlaps the top-right buttons
        surface.blit(bg, (6, HEIGHT - 170))
        surface.blit(qs, (14, HEIGHT - 167))


def draw_key_guide(surface):
    bg = pygame.Surface((260, 280), pygame.SRCALPHA)
    bg.fill((20, 15, 10, 200))
    surface.blit(bg, (WIDTH - 270, 52))
    keys = [
        "WASD / Arrows  move",
        "E              pick up",
        "F              eat food",
        "C              crafting",
        "R              deploy raft",
        "Z              throw knife",
        "T              throw spike",
        "X              swing axe",
        "O              enchant axe",
        "Q              quest log",
        "M              key guide",
        "N              toggle map",
    ]
    for i, k in enumerate(keys):
        ks = small_font.render(k, True, (200, 200, 180))
        surface.blit(ks, (WIDTH - 262, 60 + i * 24))


def draw_quest_log(surface, quest_index):
    bg = pygame.Surface((400, HEIGHT - 60), pygame.SRCALPHA)
    bg.fill((20, 15, 10, 220))
    surface.blit(bg, (WIDTH - 410, 50))
    th = instr_font.render("Quest Log", True, (255, 220, 80))
    surface.blit(th, (WIDTH - 395, 60))
    for i, q in enumerate(QUESTS):
        col = (80, 220, 80) if i < quest_index else (
            (255, 220, 80) if i == quest_index else (140, 140, 140))
        prefix = "✓ " if i < quest_index else (
            "▸ " if i == quest_index else "  ")
        qs = small_font.render(prefix + q, True, col)
        surface.blit(qs, (WIDTH - 395, 95 + i * 28))


# ─────────────────────────────────────────────
#  MINIMAP  (Minecraft-style, zoomed to player position)
# ─────────────────────────────────────────────
_MAP_W, _MAP_H = 220, 145       # size of the minimap widget
_MAP_MARGIN = 10             # distance from top-right corner
# fraction of the full map visible (smaller = more zoomed in)
_MAP_ZOOM = 0.45
_MAP_BORDER = 3

# Room positions on the hand-drawn map image (0-1 normalised)
# Estimated from the visual: house=left mainland, island=top-right
_ROOM_MAP_POS = [
    (0.18, 0.74),   # 0  Your Room      (house on mainland)
    (0.18, 0.74),   # 1  Lumi's Room    (same building)
    (0.18, 0.74),   # 2  Kitchen        (same building)
    (0.34, 0.62),   # 3  Meadow         (desert centre-left)
    (0.50, 0.60),   # 4  Desert         (cactus area)
    (0.62, 0.52),   # 5  Forest         (green patch)
    (0.72, 0.46),   # 6  Shore          (coast / water edge)
    (0.86, 0.22),   # 7  Pawbert Island (top-right island)
]


def draw_minimap(surface, current_room, map_open):
    """Draw Minecraft-style minimap in the top-right corner.

    When map_open is False:  small zoomed thumbnail.
    When map_open is True:   larger full-map overlay centred on screen.
    """
    if map_open:
        # Full map overlay — centred, larger
        mw, mh = int(map_img_raw.get_width() *
                     0.7), int(map_img_raw.get_height() * 0.7)
        mx = (WIDTH - mw) // 2
        my = (HEIGHT - mh) // 2
        # dark overlay behind the map
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        full_map = pygame.transform.smoothscale(map_img_raw, (mw, mh))
        surface.blit(full_map, (mx, my))
        pygame.draw.rect(surface, (220, 190, 100), (mx, my, mw, mh), 3)
        # player dot
        nx, ny = _ROOM_MAP_POS[min(current_room, len(_ROOM_MAP_POS)-1)]
        px = mx + int(nx * mw)
        py = my + int(ny * mh)
        pygame.draw.circle(surface, (80, 200, 80),  (px, py), 8)
        pygame.draw.circle(surface, (255, 255, 255), (px, py), 8, 2)
        # label
        lbl = small_font.render("[N] Close Map", True, (220, 220, 180))
        surface.blit(lbl, (mx + mw - lbl.get_width() - 6, my + mh + 4))
        return

    # ── small corner minimap ──
    # Determine where the player is on the map (0-1)
    nx, ny = _ROOM_MAP_POS[min(current_room, len(_ROOM_MAP_POS)-1)]

    # The zoomed crop: _MAP_ZOOM fraction of the source image, centred on player pos
    src_w = map_img_raw.get_width()
    src_h = map_img_raw.get_height()

    crop_w = int(src_w * _MAP_ZOOM)
    crop_h = int(src_h * _MAP_ZOOM)

    # centre crop on player, clamped so we don't go out of bounds
    cx = int(nx * src_w) - crop_w // 2
    cy = int(ny * src_h) - crop_h // 2
    cx = max(0, min(src_w - crop_w, cx))
    cy = max(0, min(src_h - crop_h, cy))

    crop_rect = pygame.Rect(cx, cy, crop_w, crop_h)
    cropped = map_img_raw.subsurface(crop_rect)
    scaled = pygame.transform.smoothscale(cropped, (_MAP_W, _MAP_H))

    # position: top-right corner
    mx = WIDTH - _MAP_W - _MAP_MARGIN - _MAP_BORDER * 2
    my = _MAP_MARGIN

    # border / frame
    pygame.draw.rect(surface, (30, 25, 20),
                     (mx - _MAP_BORDER, my - _MAP_BORDER,
                      _MAP_W + _MAP_BORDER * 2, _MAP_H + _MAP_BORDER * 2))
    pygame.draw.rect(surface, (200, 170, 90),
                     (mx - _MAP_BORDER, my - _MAP_BORDER,
                      _MAP_W + _MAP_BORDER * 2, _MAP_H + _MAP_BORDER * 2), 2)

    surface.blit(scaled, (mx, my))

    # player dot — always in centre of minimap because we crop around player
    dot_x = mx + _MAP_W // 2
    dot_y = my + _MAP_H // 2
    pygame.draw.circle(surface, (80, 220, 80),   (dot_x, dot_y), 5)
    pygame.draw.circle(surface, (255, 255, 255), (dot_x, dot_y), 5, 1)

    # hint text
    hint = small_font.render("[N] Map", True, (180, 170, 130))
    surface.blit(hint, (mx, my + _MAP_H + 2))


# ─────────────────────────────────────────────
#  TREE HELPER
# ─────────────────────────────────────────────
def create_trees(room_idx):
    tl = []
    for pos in ROOMS[room_idx].get("trees", []):
        tr = tree_img.copy()
        tl.append({"rect": tr.get_rect(topleft=pos), "health": 3, "img": tr})
    return tl

# ─────────────────────────────────────────────
#  ENTER ROOM
# ─────────────────────────────────────────────


def enter_room(state, new_idx, from_right):
    state["current_room"] = new_idx
    room = ROOMS[new_idx]

    # lala
    state["lala_alive"] = bool(room.get("has_lala"))
    state["lala_lives"] = room.get("lala_lives", 0)
    state["lala_rect"] = lala_img.get_rect(
        topleft=room.get("lala_pos", (0, 0)))

    # lulu (forest only)
    state["lulu_alive"] = (new_idx == 5)
    state["lulu_lives"] = 4 if new_idx == 5 else 0
    state["lulu_rect"] = lulu_img.get_rect(
        topleft=(900, 500)) if new_idx == 5 else None

    # scorpion — hidden behind cactus, only activates when cactus is picked up
    # starts hidden; triggered by cactus pickup
    state["scorpion_active"] = False
    state["scorpion_lives"] = room.get("scorpion_lives", 0)
    state["scorpion_rect"].topleft = room.get("scorpion_pos", (0, 0))

    state["poison_spews"] = []
    state["lala_slimes"] = []
    state["slime_timer"] = random.randint(SLIME_MIN_CD, SLIME_MAX_CD)

    # trees
    state["trees"] = create_trees(new_idx) if new_idx == 5 else []

    # water
    state["water_rects"] = [pygame.Rect(w) for w in room.get("water", [])]

    # spawn items once per room entry (only if not already picked up)
    room_key = f"room_{new_idx}_items_spawned"
    if not state.get(room_key):
        state[room_key] = True
        for it in room.get("items_on_enter", []):
            img = it["img"]
            state["dropped_items"].append({
                "type": it["type"],
                "rect": img.get_rect(topleft=it["pos"]),
                "img":  img,
            })

    # run intro state for this room
    intro = room.get("intro_state")
    if intro and not state.get(f"room_{new_idx}_intro_done"):
        state["game_state"] = intro
        state["dialogue_index"] = 0
        state["space_released"] = True

    # position player
    if from_right:
        player_rect.right = WIDTH - 1
    else:
        player_rect.left = 1

    state["prev_in_water"] = False
    state["room_transition_flash"] = 20  # white flash frames
    return state


# ─────────────────────────────────────────────
#  BOSS AI
# ─────────────────────────────────────────────
_pawbert_angle = 0
_pawbert_phase = 0


def update_pawbert(state):
    global _pawbert_angle, _pawbert_phase
    if not state["pawbert_active"]:
        return
    pr = state["pawbert_rect"]
    px, py = player_rect.center
    bx, by = pr.center
    dx, dy = px - bx, py - by
    dist = math.hypot(dx, dy) or 1

    # Phase-based movement: gets more aggressive as HP drops
    hp_ratio = state["pawbert_lives"] / PAWBERT_MAX_LIVES
    speed = PAWBERT_SPEED + (1 - hp_ratio) * 2.5  # faster when hurt

    # Zigzag approach
    _pawbert_angle += 0.05
    perp_x = -dy / dist
    perp_y = dx / dist
    zigzag = math.sin(_pawbert_angle * 3) * 60

    # Mix: chase player with perpendicular zigzag
    move_x = (dx / dist) * speed + perp_x * math.sin(_pawbert_angle) * 1.5
    move_y = (dy / dist) * speed + perp_y * math.sin(_pawbert_angle) * 1.5

    pr.x += int(move_x)
    pr.y += int(move_y)
    pr.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    # Pawbert attacks player on contact
    state["pawbert_atk_timer"] -= 1
    if state["pawbert_atk_timer"] <= 0:
        state["pawbert_atk_timer"] = max(
            40, PAWBERT_ATCK_CD - int((1 - hp_ratio) * 60))
        if pr.colliderect(player_rect) and not state["player_invulnerable"]:
            state["player_lives"] = max(0, state["player_lives"] - 3)
            play_sfx(SFX_HIT_DAMAGE)
            state["player_invulnerable"] = True
            state["invuln_timer"] = INVULN_FRAMES
            notify("Mr. Pawbert hit you! -3 HP")

# ─────────────────────────────────────────────
#  RUNNING SEQUENCE ANIMATION
# ─────────────────────────────────────────────


class RunningSequence:
    """Scrolling background animation with bonding dialogue."""

    def __init__(self, dialogue, name=""):
        self.dialogue = [(sp, txt.replace("{name}", name))
                         for sp, txt in dialogue]
        self.idx = 0
        self.timer = 0
        self.done = False
        self.tree_x = WIDTH + 100
        self.tree2_x = WIDTH + 400

    def update(self):
        self.tree_x -= 3
        self.tree2_x -= 2
        if self.tree_x < -100:
            self.tree_x = WIDTH + random.randint(50, 200)
        if self.tree2_x < -100:
            self.tree2_x = WIDTH + random.randint(100, 300)

    def draw(self, surface):
        # scrolling bg
        surface.blit(running_bg, (0, 0))
        # Ground
        pygame.draw.rect(surface, (50, 90, 35), (0, HEIGHT - 140, WIDTH, 140))
        pygame.draw.rect(surface, (70, 130, 50), (0, HEIGHT - 145, WIDTH, 10))
        # Scrolling trees (parallax)
        surface.blit(tree_img, (int(self.tree_x),
                     HEIGHT - 145 - tree_img.get_height()))
        surface.blit(tree_img, (int(self.tree2_x), HEIGHT -
                     145 - tree_img.get_height() + 20))
        # Dust puffs
        t_ms3 = pygame.time.get_ticks()
        for di in range(4):
            dx = (200 + di * 40 - (t_ms3 // 8) % 240) % 500
            dy = HEIGHT - 145 + 4
            alpha = max(0, 160 - di * 35)
            dust = pygame.Surface((20, 10), pygame.SRCALPHA)
            dust.fill((200, 180, 140, alpha))
            surface.blit(dust, (dx, dy))
        # Player running (bob up and down)
        bob = int(math.sin(t_ms3 / 120) * 6)
        surface.blit(player, (160, HEIGHT - 145 - player_rect.height + bob))
        # Lala running alongside (offset bob)
        bob2 = int(math.sin(t_ms3 / 120 + 1.5) * 6)
        surface.blit(lala_img, (300, HEIGHT - 145 -
                     lala_img.get_height() + bob2))

    def advance(self):
        self.idx += 1
        if self.idx >= len(self.dialogue):
            self.done = True

    def current(self):
        if self.idx < len(self.dialogue):
            return self.dialogue[self.idx]
        return None, None


running_seq = None   # created when needed

# ─────────────────────────────────────────────
#  GAME STATE
# ─────────────────────────────────────────────


def make_initial_state(player_name="Hero"):
    inv = [None] * INV_SLOTS
    # inventory starts empty — knife is picked up in kitchen

    pawbert_rect = pygame.Surface((80, 120), pygame.SRCALPHA)
    pawbert_rect.fill((200, 50, 50))
    pr = pawbert_rect.get_rect(topleft=(900, 400))

    state = {
        "player_name":        player_name,
        "game_state":         "start_screen",
        "current_room":       0,
        "dialogue_index":     0,
        "space_released":     True,
        "player_lives":       3,
        "max_player_lives":   3,
        "facing":             "right",
        "speed":              5,
        "inventory":          inv,
        "equipped_index":     0,
        "dropped_items":      [],
        "knives":             [],
        "spikes":             [],
        "lala_alive":         False,
        "lala_lives":         0,
        "lala_rect":          lala_img.get_rect(topleft=(800, 500)),
        "lulu_alive":         False,
        "lulu_lives":         0,
        "lulu_rect":          None,
        "scorpion_active":    False,
        "scorpion_rect":      scorpion_img.get_rect(topleft=(600, 580)),
        "scorpion_lives":     0,
        "scorpion_ever_killed": False,
        "poison_spews":       [],
        "lala_slimes":        [],
        "slime_timer":        random.randint(SLIME_MIN_CD, SLIME_MAX_CD),
        "player_invulnerable": False,
        "invuln_timer":       0,
        "axe_timer":          0,
        "axe_enchanted":      False,
        "axe_enchant_timer":  0,
        "poisoned":           False,
        "poison_timer":       0,
        "poison_tick":        0,
        "water_rects":        [],
        "in_water":           False,
        "prev_in_water":      False,
        "breath":             BREATH_MAX,
        "trees":              [],
        "raft_objects":       [],
        "raft_crafting":      False,
        "raft_palette":       [],
        "placed_planks":      [],
        "selected_plank":     None,
        "is_crafting_open":   False,
        "is_quest_log_open":  False,
        "is_key_guide_open":  False,
        "quest_index":        0,
        "postfight_done":     False,
        "player_trusts_lala": None,
        "lulu_trusts":        None,
        "selected_choice":    0,
        "first_fight_done":   False,
        "lala_joined":        False,
        "lala_surrendered":   False,
        "lulu_joined":        False,
        "raft_crossed":       False,
        "pawbert_active":     False,
        "pawbert_surf":       pawbert_rect,
        "pawbert_rect":       pr,
        "pawbert_lives":      PAWBERT_MAX_LIVES,
        "pawbert_atk_timer":  PAWBERT_ATCK_CD,
        "boss_lalas_active":  False,
        "boss_lala_list":     [],
        "ally_lala_list":     [],
        "dialogue_choices":   [],
        "room_transition_flash": 0,
        "map_open":              False,
        "death_count":           0,
    }
    return state


def reset_player_pos(state, side="left"):
    if side == "left":
        player_rect.bottomleft = (100, HEIGHT - 20)
    else:
        player_rect.bottomright = (WIDTH - 100, HEIGHT - 20)


# ─────────────────────────────────────────────
#  DRAW BOSS LALAS  (enemy side during boss fight)
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  BOSS LALAS  (enemy side during boss fight)
# ─────────────────────────────────────────────
BOSS_LALA_START_POSITIONS = [
    (700, 300), (780, 340), (860, 300), (940, 340), (1020, 300),
    (700, 420), (780, 460), (860, 420), (940, 460), (1020, 420),
]


def init_boss_lalas():
    """Create the boss lala army with health and position."""
    return [{"pos": list(p), "hp": 3, "alive": True,
             "atk_timer": random.randint(60, 180)}
            for p in BOSS_LALA_START_POSITIONS]


def update_boss_lalas(state):
    """Boss LaLas attack allied LaLa (Rocky) and allied LaLas fight back."""
    if not state.get("boss_lala_list"):
        return
    ally_pos = state["lala_rect"].center if state.get("lala_alive") else None

    # Allied LaLas (Lulu's group) attack the enemy LaLas
    if state.get("ally_lala_list"):
        for al in state["ally_lala_list"]:
            if not al["alive"]:
                continue
            al["atk_timer"] -= 1
            # Find nearest enemy boss lala
            nearest_enemy = None
            nearest_dist = 999999
            for bl in state["boss_lala_list"]:
                if not bl["alive"]:
                    continue
                d = math.hypot(bl["pos"][0]-al["pos"][0],
                               bl["pos"][1]-al["pos"][1])
                if d < nearest_dist:
                    nearest_dist, nearest_enemy = d, bl
            if nearest_enemy:
                dx = nearest_enemy["pos"][0] - al["pos"][0]
                dy = nearest_enemy["pos"][1] - al["pos"][1]
                dist = math.hypot(dx, dy) or 1
                # Move toward enemy
                if dist > 50:
                    al["pos"][0] += dx / dist * 1.2
                    al["pos"][1] += dy / dist * 1.2
                # Attack if close enough
                if al["atk_timer"] <= 0 and dist < 60:
                    nearest_enemy["hp"] = max(0, nearest_enemy["hp"] - 1)
                    al["atk_timer"] = random.randint(80, 160)
                    if nearest_enemy["hp"] <= 0:
                        nearest_enemy["alive"] = False

    # Enemy boss LaLas drift toward ally Rocky
    for bl in state["boss_lala_list"]:
        if not bl["alive"]:
            continue
        bl["atk_timer"] -= 1
        if ally_pos:
            dx = ally_pos[0] - bl["pos"][0]
            dy = ally_pos[1] - bl["pos"][1]
            dist = math.hypot(dx, dy) or 1
            if dist > 60:
                bl["pos"][0] += dx / dist * 0.8
                bl["pos"][1] += dy / dist * 0.8


def draw_boss_lalas(surface, boss_lala_list=None):
    if boss_lala_list:
        for bl in boss_lala_list:
            if bl["alive"]:
                surface.blit(lala_img, (int(bl["pos"][0]), int(bl["pos"][1])))
                # tiny hp bar
                hp_w = lala_img.get_width()
                pygame.draw.rect(surface, (60, 60, 60),
                                 (int(bl["pos"][0]), int(bl["pos"][1]) - 8, hp_w, 4))
                pygame.draw.rect(surface, (200, 80, 80),
                                 (int(bl["pos"][0]), int(bl["pos"][1]) - 8,
                                  int(hp_w * bl["hp"] / 3), 4))
    else:
        # Fallback: static positions
        for pos in BOSS_LALA_START_POSITIONS:
            surface.blit(lala_img, pos)


def draw_ally_lalas(surface, ally_lala_list):
    """Draw the allied LaLas (Lulu's group) fighting on the player's side."""
    if not ally_lala_list:
        return
    for al in ally_lala_list:
        if al["alive"]:
            # Draw with a green tint to distinguish from enemies
            tinted = lulu_img.copy()
            surface.blit(tinted, (int(al["pos"][0]), int(al["pos"][1])))
            hp_w = lulu_img.get_width()
            pygame.draw.rect(surface, (60, 60, 60),
                             (int(al["pos"][0]), int(al["pos"][1]) - 8, hp_w, 4))
            pygame.draw.rect(surface, (60, 200, 80),
                             (int(al["pos"][0]), int(al["pos"][1]) - 8,
                              int(hp_w * al["hp"] / 3), 4))


def init_ally_lalas():
    """Create 10 ally LaLas from Lulu's group positioned on the left."""
    positions = [
        (80, 300), (160, 340), (80, 420), (160, 460), (80, 520),
        (240, 300), (240, 420), (320, 360), (320, 460), (400, 380),
    ]
    return [{"pos": list(p), "hp": 3, "alive": True, "atk_timer": random.randint(60, 180)}
            for p in positions]


# ─────────────────────────────────────────────
#  STAR CONFETTI
# ─────────────────────────────────────────────
confetti = []


def spawn_confetti():
    for _ in range(60):
        confetti.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(-HEIGHT, 0),
            "vy": random.uniform(2, 6),
            "vx": random.uniform(-1, 1),
            "color": random.choice([(255, 220, 50), (80, 220, 100), (100, 180, 255), (255, 100, 180), (200, 255, 80)]),
            "size": random.randint(6, 16),
        })


def draw_confetti(surface):
    for c in confetti:
        c["y"] += c["vy"]
        c["x"] += c["vx"]
        pygame.draw.circle(surface, c["color"],
                           (int(c["x"]), int(c["y"])), c["size"])
    confetti[:] = [c for c in confetti if c["y"] < HEIGHT + 20]


# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
state = make_initial_state()
run = True

# UI button rects  — positioned to the left of the minimap
QUEST_BTN = pygame.Rect(WIDTH - 395, 10, 145, 35)
KEYS_BTN = pygame.Rect(WIDTH - 395, 50, 145, 35)


def draw_ui_buttons(surface):
    pygame.draw.rect(surface, (180, 140, 60), QUEST_BTN)
    pygame.draw.rect(surface, (60, 100, 180), KEYS_BTN)
    surface.blit(font.render("Q Quest Log", True, (20, 20, 20)),
                 (QUEST_BTN.x+6, QUEST_BTN.y+8))
    surface.blit(font.render("M Key Guide", True, (220, 220, 220)),
                 (KEYS_BTN.x+6, KEYS_BTN.y+8))


def _trigger_lala_surrender(state):
    """LaLa reaches 1 HP in kitchen — stops fight, postfight dialogue starts."""
    if state.get("lala_surrendered"):
        return
    state["lala_surrendered"] = True
    state["lala_alive"] = False
    state["lala_lives"] = 1
    state["game_state"] = "postfight_dialogue"
    state["dialogue_index"] = 0
    state["space_released"] = True
    state["quest_index"] = max(state["quest_index"], 2)


# initialise mini-player rects so event loop can reference them before first draw
mp_play_rect   = pygame.Rect(0, 0, 0, 0)
mp_slider_rect = pygame.Rect(0, 0, 0, 0)
mp_slider_coords = (0, 0, 1, 1)

while run:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    keys_held = pygame.key.get_pressed()
    gs = state["game_state"]

    # ── draw background ──────────────────────
    room = ROOMS[state["current_room"]]
    screen.blit(room["bg"], (0, 0))

    # ── update player animation ──────────────
    player_image_name, active_player_frame_index = update_player_anim(
        move_direction, active_player_frame_index)
    if player_image_name in player_frames:
        player = player_frames[player_image_name]

    # ════════════════════════════════════════
    #  EVENT HANDLING
    # ════════════════════════════════════════
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # ── Global UI buttons ────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            if QUEST_BTN.collidepoint(event.pos):
                state["is_quest_log_open"] = not state["is_quest_log_open"]
                play_sfx(SFX_UI_CLICK)
            if KEYS_BTN.collidepoint(event.pos):
                state["is_key_guide_open"] = not state["is_key_guide_open"]
                play_sfx(SFX_UI_CLICK)
            # Mini-player clicks
            if event.button == 1:
                if mp_play_rect.collidepoint(event.pos):
                    music_toggle()
                elif mp_slider_rect.collidepoint(event.pos):
                    bx, _, bw, _ = mp_slider_coords
                    rel = (event.pos[0] - bx) / bw
                    music_set_volume(rel)
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if mp_slider_rect.collidepoint(event.pos):
                bx, _, bw, _ = mp_slider_coords
                rel = (event.pos[0] - bx) / bw
                music_set_volume(rel)

        # ── Global map toggle (N) ────────────
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            state["map_open"] = not state.get("map_open", False)

        # ════════════════════════════════════
        #  START SCREEN
        # ════════════════════════════════════
        if gs == "start_screen":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                state["game_state"] = "name_input"

        # ════════════════════════════════════
        #  NAME INPUT
        # ════════════════════════════════════
        elif gs == "name_input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = state.get("_name_buf", "").strip() or "Hero"
                    state["player_name"] = name
                    state["game_state"] = "intro"
                    state["dialogue_index"] = 0
                    # allow SPACE immediately in intro
                    state["space_released"] = True
                    state["dropped_items"] = []
                elif event.key == pygame.K_BACKSPACE:
                    state["_name_buf"] = state.get("_name_buf", "")[:-1]
                else:
                    ch = event.unicode
                    if ch.isprintable() and len(state.get("_name_buf", "")) < 12:
                        state["_name_buf"] = state.get("_name_buf", "") + ch

        # ════════════════════════════════════
        #  INTRO DIALOGUE  (player's room)
        # ════════════════════════════════════
        elif gs == "intro":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                state["dialogue_index"] += 1
                if state["dialogue_index"] >= len(INTRO_DIALOGUE):
                    state["game_state"] = "main"
                    state["room_0_intro_done"] = True
                    state["space_released"] = True

        # ════════════════════════════════════
        #  LUMI'S ROOM DIALOGUE  (discover Lumi is missing)
        # ════════════════════════════════════
        elif gs == "lumi_room_dialogue":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                state["dialogue_index"] += 1
                if state["dialogue_index"] >= len(LUMI_ROOM_DIALOGUE):
                    state["game_state"] = "main"
                    state["room_1_intro_done"] = True
                    state["lumi_room_done"] = True
                    state["space_released"] = True
                    state["quest_index"] = max(
                        state["quest_index"], 1)  # grab the knife

        # ════════════════════════════════════
        #  KITCHEN DIALOGUE  (first LaLa encounter)
        # ════════════════════════════════════
        elif gs == "kitchen_dialogue":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(KITCHEN_DIALOGUE):
                    # Start the fight with the LaLa
                    state["game_state"] = "main"
                    state["lala_alive"] = True
                    state["lala_lives"] = 3
                    state["lala_rect"] = lala_img.get_rect(topleft=(700, 500))
                    state["quest_index"] = max(
                        state["quest_index"], 2)  # Fight the intruder
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  POSTFIGHT DIALOGUE
        # ════════════════════════════════════
        elif gs == "postfight_dialogue":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(POSTFIGHT_DIALOGUE):
                    state["game_state"] = "dialogue_choice"
                    state["dialogue_choices"] = POSTFIGHT_CHOICES
                    state["selected_choice"] = 0
                    # BUG FIX: was == instead of =
                    state["postfight_done"] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  DIALOGUE CHOICE
        # ════════════════════════════════════
        elif gs == "dialogue_choice":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    state["selected_choice"] = (
                        state["selected_choice"] - 1) % len(state["dialogue_choices"])
                if event.key == pygame.K_DOWN:
                    state["selected_choice"] = (
                        state["selected_choice"] + 1) % len(state["dialogue_choices"])
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    choice = state["selected_choice"]
                    # Determine which choice set we're in
                    if state["dialogue_choices"] == POSTFIGHT_CHOICES:
                        state["player_trusts_lala"] = (choice == 0)
                        if choice == 0:
                            notify("Rocky will help you!")
                            state["lala_joined"] = True
                            state["quest_index"] = 3   # Follow LaLa
                        else:
                            notify(
                                "You chose not to trust Rocky. Rocky follows anyway...")
                            # Rocky joins regardless for story
                            state["lala_joined"] = True
                            state["quest_index"] = 3
                        state["game_state"] = "running_sequence"
                        state["room_0_intro_done"] = True
                        state["postfight_dialogue_done"] = True
                        running_seq = RunningSequence(
                            RUNNING_DIALOGUE, state["player_name"])
                    elif state["dialogue_choices"] == LULU_CHOICES:
                        state["lulu_trusts"] = (choice == 0)
                        if choice == 0:
                            state["lulu_joined"] = True
                            notify("LuLu and the LaLas join you!")
                            # Follow Rocky → craft axe
                            state["quest_index"] = max(state["quest_index"], 7)
                        else:
                            notify(
                                "You declined their help... but they follow anyway!")
                            state["lulu_joined"] = True  # Story requires it
                            state["quest_index"] = max(state["quest_index"], 7)
                        state["game_state"] = "main"
                        state[f"room_5_intro_done"] = True

        # ════════════════════════════════════
        #  RUNNING SEQUENCE
        # ════════════════════════════════════
        elif gs == "running_sequence":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                running_seq.advance()
                state["space_released"] = False
                if running_seq.done:
                    state["game_state"] = "main"
                    state["_running_done"] = True
                    state["quest_index"] = max(
                        state["quest_index"], 4)  # eat cactus
                    # Knife was left behind before the journey — remove from inventory
                    state["inventory"] = [s if (s is None or s.get("type") != ITEM_KNIFE) else None
                                          for s in state["inventory"]]
                    # move to next room (desert area)
                    enter_room(state, 4, from_right=False)
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  DESERT DIALOGUE
        # ════════════════════════════════════
        elif gs == "desert_dialogue":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(DESERT_DIALOGUE):
                    state["game_state"] = "main"
                    state[f"room_4_intro_done"] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  FOREST DIALOGUE  (LuLu encounter)
        # ════════════════════════════════════
        elif gs == "forest_dialogue":
            # show lulu dialogue part 1
            full = LULU_DIALOGUE_1 + LULU_DIALOGUE_2
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(LULU_DIALOGUE_1):
                    state["game_state"] = "forest_dialogue_2"
                    state["dialogue_index"] = 0
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        elif gs == "forest_dialogue_2":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(LULU_DIALOGUE_2):
                    state["game_state"] = "dialogue_choice"
                    state["dialogue_choices"] = LULU_CHOICES
                    state["selected_choice"] = 0
                    state["dialogue_index"] = 0
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  SHORE DIALOGUE
        # ════════════════════════════════════
        elif gs == "shore_dialogue":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(SHORE_DIALOGUE):
                    state["game_state"] = "main"
                    state[f"room_6_intro_done"] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  BOSS DIALOGUE
        # ════════════════════════════════════
        elif gs == "boss_dialogue":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(BOSS_DIALOGUE):
                    # LaLa gives you the Krypton before the fight!
                    add_item(state["inventory"], ITEM_KRYPTON)
                    notify("Rocky hands you the Krypton! Enchant your axe with O!")
                    state["game_state"] = "boss_fight"
                    state["pawbert_active"] = True
                    state["boss_lalas_active"] = True
                    state["boss_lala_list"] = init_boss_lalas()
                    state["ally_lala_list"] = init_ally_lalas()
                    state[f"room_7_intro_done"] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  BOSS FIGHT  (combat keys)
        # ════════════════════════════════════
        elif gs == "boss_fight":
            if event.type == pygame.KEYDOWN:
                # Enchant axe (O)
                if event.key == pygame.K_o:
                    if (count_item(state["inventory"], ITEM_AXE) >= 1
                            and count_item(state["inventory"], ITEM_KRYPTON) >= 1
                            and not state["axe_enchanted"]):
                        consume_items(state["inventory"], {ITEM_KRYPTON: 1})
                        state["axe_enchanted"] = True
                        state["axe_enchant_timer"] = AXE_ENCHANT_DURATION
                        play_sfx(SFX_ENCHANT)
                        notify("Axe ENCHANTED with Krypton!")
                        if state["quest_index"] == 10:
                            state["quest_index"] = 11
                    elif state["axe_enchanted"]:
                        notify("Axe is already enchanted!")
                    elif count_item(state["inventory"], ITEM_AXE) < 1:
                        notify("You need an axe to enchant!")
                    else:
                        notify("You need Krypton to enchant!")
                # Swing axe (X)
                if event.key == pygame.K_x:
                    if (get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_AXE
                            and state["axe_timer"] <= 0):
                        eff = AXE_DAMAGE + \
                            (AXE_ENCHANT_BONUS if state["axe_enchanted"] else 0)
                        if state["facing"] == "right":
                            swing = pygame.Rect(player_rect.right,
                                                player_rect.centery - AXE_HEIGHT // 2,
                                                AXE_RANGE, AXE_HEIGHT)
                        else:
                            swing = pygame.Rect(player_rect.left - AXE_RANGE,
                                                player_rect.centery - AXE_HEIGHT // 2,
                                                AXE_RANGE, AXE_HEIGHT)
                        if state["pawbert_active"] and swing.colliderect(state["pawbert_rect"]):
                            state["pawbert_lives"] = max(
                                0, state["pawbert_lives"] - eff)
                            if state["pawbert_lives"] <= 0:
                                state["pawbert_active"] = False
                                state["game_state"] = "final_dialogue"
                                state["dialogue_index"] = 0
                                state["quest_index"] = max(
                                    state["quest_index"], 12)
                        state["axe_timer"] = AXE_COOLDOWN
                # Throw knife (Z)
                if event.key == pygame.K_z and len(state["knives"]) < MAX_KNIVES:
                    if get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_KNIFE:
                        vx = KNIFE_SPEED if state["facing"] == "right" else -KNIFE_SPEED
                        kr = knife_img.get_rect(center=player_rect.center)
                        if vx > 0:
                            kr.left = player_rect.right
                        else:
                            kr.right = player_rect.left
                        state["knives"].append({"rect": kr, "vx": vx})
                        play_sfx(SFX_THROW)
                # Throw spike (T)
                if event.key == pygame.K_t and len(state["spikes"]) < MAX_SPIKES:
                    if get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_SPIKE:
                        vx = SPIKE_SPEED if state["facing"] == "right" else -SPIKE_SPEED
                        sr = spike_img.get_rect(center=player_rect.center)
                        if vx > 0:
                            sr.left = player_rect.right
                        else:
                            sr.right = player_rect.left
                        state["spikes"].append({"rect": sr, "vx": vx})
                        play_sfx(SFX_THROW)
                if pygame.K_1 <= event.key <= pygame.K_5:
                    state["equipped_index"] = event.key - pygame.K_1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(get_inventory_rects()):
                    if rect.collidepoint(event.pos):
                        state["equipped_index"] = i

        # ════════════════════════════════════
        #  FINAL DIALOGUE
        # ════════════════════════════════════
        elif gs == "final_dialogue":
            txt = [(sp, t.replace("{name}", state["player_name"]))
                   for sp, t in FINAL_DIALOGUE]
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                    and state["space_released"]):
                state["dialogue_index"] += 1
                state["space_released"] = False
                if state["dialogue_index"] >= len(txt):
                    state["game_state"] = "victory"
                    state["quest_index"] = max(state["quest_index"], 12)
                    spawn_confetti()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                state["space_released"] = True

        # ════════════════════════════════════
        #  DEATH / VICTORY screens
        # ════════════════════════════════════
        elif gs == "death":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                state = make_initial_state(state["player_name"])
                player_rect.bottomleft = (100, HEIGHT - 20)

        elif gs == "victory":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                state = make_initial_state(state["player_name"])
                player_rect.bottomleft = (100, HEIGHT - 20)

        # ════════════════════════════════════
        #  MAIN  (gameplay)
        # ════════════════════════════════════
        elif gs == "main":
            if event.type == pygame.KEYDOWN:
                # Pick up
                if event.key == pygame.K_e:
                    ITEM_NAMES = {
                        ITEM_KNIFE: "Knife", ITEM_CACTUS: "Cactus Fruit",
                        ITEM_SPIKE: "Spike", ITEM_WOOD: "Wood",
                        ITEM_STONE: "Stone", ITEM_AXE: "Axe",
                        ITEM_RAFT: "Raft", ITEM_RESIN: "Resin",
                        ITEM_KRYPTON: "Krypton"
                    }
                    for i, item in enumerate(state["dropped_items"]):
                        if player_rect.inflate(40, 40).colliderect(item["rect"]):
                            leftover = add_item(
                                state["inventory"], item["type"])
                            if leftover == 0:
                                name = ITEM_NAMES.get(item["type"], "item")
                                state["dropped_items"].pop(i)
                                notify(f"Picked up {name}!")
                                # Quest tracking
                                if item["type"] == ITEM_KNIFE and state["quest_index"] == 1:
                                    state["quest_index"] = 2
                                if item["type"] == ITEM_WOOD and state["quest_index"] == 6:
                                    state["quest_index"] = 7
                                # Cactus pickup triggers scorpion to appear!
                                if item["type"] == ITEM_CACTUS and not state.get("scorpion_ever_killed"):
                                    room_now = ROOMS[state["current_room"]]
                                    if room_now.get("has_scorpion"):
                                        state["scorpion_active"] = True
                                        state["scorpion_lives"] = room_now.get(
                                            "scorpion_lives", 5)
                                        state["scorpion_rect"].topleft = room_now.get(
                                            "scorpion_pos", (700, 580))
                                        play_sfx(SFX_SCORPION)
                                        notify(
                                            "A scorpion was hiding behind the cactus!")
                            else:
                                notify("Inventory full!")
                            break

                # Eat
                if event.key == pygame.K_f:
                    if get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_CACTUS:
                        remove_one(state["inventory"], state["equipped_index"])
                        state["player_lives"] = min(
                            state["player_lives"] + 1, state["max_player_lives"])
                        play_sfx(SFX_EAT)
                        notify("Healed +1 HP!")
                        if state["quest_index"] == 4:
                            state["quest_index"] = 5

                # Crafting toggle
                if event.key == pygame.K_c:
                    state["is_crafting_open"] = not state["is_crafting_open"]

                # Drop
                if event.key == pygame.K_g:
                    slot = state["inventory"][state["equipped_index"]]
                    if slot:
                        dt = slot["type"]
                        remove_one(state["inventory"], state["equipped_index"])
                        dimg = item_imgs[dt] if dt < len(
                            item_imgs) else knife_img
                        state["dropped_items"].append({
                            "type": dt,
                            "rect": dimg.get_rect(topleft=(player_rect.centerx, player_rect.centery)),
                            "img":  dimg if isinstance(dimg, pygame.Surface) else knife_img,
                        })

                # Throw knife
                if event.key == pygame.K_z and len(state["knives"]) < MAX_KNIVES:
                    if get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_KNIFE:
                        vx = KNIFE_SPEED if state["facing"] == "right" else -KNIFE_SPEED
                        kr = knife_img.get_rect(center=player_rect.center)
                        if vx > 0:
                            kr.left = player_rect.right
                        else:
                            kr.right = player_rect.left
                        state["knives"].append({"rect": kr, "vx": vx})
                        play_sfx(SFX_THROW)

                # Throw spike
                if event.key == pygame.K_t and len(state["spikes"]) < MAX_SPIKES:
                    if get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_SPIKE:
                        vx = SPIKE_SPEED if state["facing"] == "right" else -SPIKE_SPEED
                        sr = spike_img.get_rect(center=player_rect.center)
                        if vx > 0:
                            sr.left = player_rect.right
                        else:
                            sr.right = player_rect.left
                        state["spikes"].append({"rect": sr, "vx": vx})
                        play_sfx(SFX_THROW)

                # Swing axe (X)
                if event.key == pygame.K_x:
                    if (get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_AXE
                            and state["axe_timer"] <= 0):
                        eff = AXE_DAMAGE + \
                            (AXE_ENCHANT_BONUS if state["axe_enchanted"] else 0)
                        if state["facing"] == "right":
                            swing = pygame.Rect(player_rect.right,
                                                player_rect.centery - AXE_HEIGHT // 2,
                                                AXE_RANGE, AXE_HEIGHT)
                        else:
                            swing = pygame.Rect(player_rect.left - AXE_RANGE,
                                                player_rect.centery - AXE_HEIGHT // 2,
                                                AXE_RANGE, AXE_HEIGHT)
                        if state["lala_alive"] and swing.colliderect(state["lala_rect"]):
                            if state["current_room"] == 2:
                                state["lala_lives"] = max(
                                    1, state["lala_lives"] - eff)
                                if state["lala_lives"] <= 1:
                                    _trigger_lala_surrender(state)
                            else:
                                state["lala_lives"] = max(
                                    0, state["lala_lives"] - eff)
                                if state["lala_lives"] <= 0:
                                    state["lala_alive"] = False
                                    play_sfx(SFX_ENEMY_WIN)
                        if state["lulu_alive"] and state["lulu_rect"] and swing.colliderect(state["lulu_rect"]):
                            if state["current_room"] == 5:
                                # Can't hurt forest LaLas — they're friendly!
                                notify("They're on your side!")
                            else:
                                state["lulu_lives"] = max(
                                    0, state["lulu_lives"] - eff)
                                if state["lulu_lives"] <= 0:
                                    state["lulu_alive"] = False
                                    play_sfx(SFX_ENEMY_WIN)
                        if state["scorpion_active"] and swing.colliderect(state["scorpion_rect"]):
                            state["scorpion_lives"] = max(
                                0, state["scorpion_lives"] - eff)
                            if state["scorpion_lives"] <= 0:
                                state["scorpion_active"] = False
                                state["scorpion_ever_killed"] = True
                                play_sfx(SFX_ENEMY_WIN)
                                if state["quest_index"] == 5:
                                    state["quest_index"] = 6
                        if state["pawbert_active"] and swing.colliderect(state["pawbert_rect"]):
                            state["pawbert_lives"] = max(
                                0, state["pawbert_lives"] - eff)
                            if state["pawbert_lives"] <= 0:
                                state["pawbert_active"] = False
                                play_sfx(SFX_ENEMY_WIN)
                                state["game_state"] = "final_dialogue"
                                state["dialogue_index"] = 0
                                state["quest_index"] = max(
                                    state["quest_index"], 12)
                        # chop trees
                        for t in state["trees"][:]:
                            if swing.colliderect(t["rect"]):
                                t["health"] -= 1
                                play_sfx(SFX_CHOP)
                                notify("*chop!*")
                                if t["health"] <= 0:
                                    state["trees"].remove(t)
                                    wood_amt = random.randint(2, 3)
                                    add_item(state["inventory"],
                                             ITEM_WOOD, wood_amt)
                                    notify(f"+{wood_amt} Wood!")
                                    if random.random() < 0.65:
                                        add_item(
                                            state["inventory"], ITEM_RESIN)
                                        notify("+1 Resin!")
                                    if state["quest_index"] == 7:
                                        state["quest_index"] = 8
                        state["axe_timer"] = AXE_COOLDOWN

                # Enchant axe (O)
                if event.key == pygame.K_o:
                    if (count_item(state["inventory"], ITEM_AXE) >= 1
                            and count_item(state["inventory"], ITEM_KRYPTON) >= 1
                            and not state["axe_enchanted"]):
                        consume_items(state["inventory"], {ITEM_KRYPTON: 1})
                        state["axe_enchanted"] = True
                        state["axe_enchant_timer"] = AXE_ENCHANT_DURATION
                        play_sfx(SFX_ENCHANT)
                        notify("Axe ENCHANTED with Krypton!")
                        if state["quest_index"] == 10:
                            state["quest_index"] = 11

                # Deploy raft (R)
                if event.key == pygame.K_r:
                    if count_item(state["inventory"], ITEM_RAFT) >= 1:
                        consume_items(state["inventory"], {ITEM_RAFT: 1})
                        rx = player_rect.centerx - 60
                        ry = max(0, player_rect.bottom - 30)
                        state["raft_objects"].append(
                            {"rect": pygame.Rect(rx, ry, 120, 40)})
                        notify("Raft deployed! Stand on it to cross the water.")
                    else:
                        notify("No raft in inventory!")

                # Quest log (Q)
                if event.key == pygame.K_q:
                    state["is_quest_log_open"] = not state["is_quest_log_open"]
                    play_sfx(SFX_UI_CLICK)
                # Key guide (M)
                if event.key == pygame.K_m:
                    state["is_key_guide_open"] = not state["is_key_guide_open"]
                    play_sfx(SFX_UI_CLICK)
        # Map toggle (N)
                if event.key == pygame.K_n:
                    state["map_open"] = not state.get("map_open", False)
                # Close map with Escape too
                if event.key == pygame.K_ESCAPE:
                    state["map_open"] = False

            # Mouse click (inventory + crafting)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # inventory slot select
                for i, rect in enumerate(get_inventory_rects()):
                    if rect.collidepoint(event.pos):
                        state["equipped_index"] = i
                # crafting buttons
                if state["is_crafting_open"]:
                    btn_r, raft_r = display_crafting_panel(screen, state["inventory"],
                                                           state["axe_enchanted"], state["axe_enchant_timer"])
                    if btn_r.collidepoint(event.pos):
                        if do_craft_axe(state["inventory"], state["dropped_items"]):
                            if state["quest_index"] == 7:
                                state["quest_index"] = 8
                    if raft_r.collidepoint(event.pos):
                        ok, pal, planks, sel = start_raft_crafting(
                            state["inventory"])
                        if ok:
                            state["raft_crafting"] = True
                            state["raft_palette"] = pal
                            state["placed_planks"] = planks
                            state["selected_plank"] = sel
                            state["is_crafting_open"] = False
                # tree chopping (left click)
                if not state["is_crafting_open"]:
                    for t in state["trees"][:]:
                        if t["rect"].collidepoint(event.pos):
                            if get_slot_type(state["inventory"], state["equipped_index"]) == ITEM_AXE:
                                dist = math.hypot(player_rect.centerx - t["rect"].centerx,
                                                  player_rect.centery - t["rect"].centery)
                                if dist <= 160:
                                    t["health"] -= 1
                                    play_sfx(SFX_CHOP)
                                    if t["health"] <= 0:
                                        state["trees"].remove(t)
                                        amt = random.randint(1, 3)
                                        add_item(
                                            state["inventory"], ITEM_WOOD, amt)
                                        notify(f"+{amt} Wood!")
                            else:
                                notify("Equip your axe to chop trees!")

            if event.type == pygame.KEYUP:
                still_moving = any([
                    keys_held[pygame.K_RIGHT], keys_held[pygame.K_d],
                    keys_held[pygame.K_LEFT],  keys_held[pygame.K_a],
                    keys_held[pygame.K_UP],    keys_held[pygame.K_w],
                    keys_held[pygame.K_DOWN],  keys_held[pygame.K_s],
                ])
                if not still_moving:
                    move_direction = MoveDirection.MOVE_DOWN

        # ── raft crafting mini-game ──────────
        if state["raft_crafting"]:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                picked = None
                for p in state["raft_palette"]:
                    if not p["used"] and p["rect"].collidepoint(pos):
                        picked = p
                        break
                if picked:
                    r = plank_img.get_rect(center=pos)
                    state["placed_planks"].append(
                        {"rect": r, "angle": 0, "snapped": False})
                    picked["used"] = True
                    state["selected_plank"] = state["placed_planks"][-1]
                    play_sfx(SFX_RAFT_PLACE)
                else:
                    for pl in reversed(state["placed_planks"]):
                        if pl["rect"].collidepoint(pos):
                            state["selected_plank"] = pl
                            break
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                state["selected_plank"] = None
            if event.type == pygame.MOUSEMOTION and state["selected_plank"]:
                mx, my = event.pos
                state["selected_plank"]["rect"].center = (mx, my)
                snap = find_nearest_snap((mx, my))
                if snap:
                    state["selected_plank"]["rect"].center = snap
                    state["selected_plank"]["snapped"] = True
                else:
                    state["selected_plank"]["snapped"] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and state["selected_plank"]:
                    state["selected_plank"]["angle"] = (
                        state["selected_plank"]["angle"] - 90) % 360
                if event.key == pygame.K_e and state["selected_plank"]:
                    state["selected_plank"]["angle"] = (
                        state["selected_plank"]["angle"] + 90) % 360
                if event.key == pygame.K_t:
                    if finish_raft(state["inventory"], state["placed_planks"]):
                        state["raft_crafting"] = False
                        if state["quest_index"] == 8:
                            state["quest_index"] = 9
                if event.key == pygame.K_ESCAPE:
                    state["raft_crafting"] = False

    # ════════════════════════════════════════
    # ════════════════════════════════════════
    #  PHYSICS / GAME LOGIC  (runs every frame)
    # ════════════════════════════════════════
    gs = state["game_state"]   # refresh after event handling

    # ── movement ────────────────────────────
    if gs in ("main", "boss_fight"):
        spd = state["speed"]
        moved = False
        if keys_held[pygame.K_RIGHT] or keys_held[pygame.K_d]:
            player_rect.x += spd
            state["facing"] = "right"
            move_direction = MoveDirection.MOVE_RIGHT
            moved = True
        if keys_held[pygame.K_LEFT] or keys_held[pygame.K_a]:
            player_rect.x -= spd
            state["facing"] = "left"
            move_direction = MoveDirection.MOVE_LEFT
            moved = True
        if (keys_held[pygame.K_UP] or keys_held[pygame.K_w]) and player_rect.y > 220:
            player_rect.y -= spd
            move_direction = MoveDirection.MOVE_UP
            moved = True
        if keys_held[pygame.K_DOWN] or keys_held[pygame.K_s]:
            player_rect.y += spd
            move_direction = MoveDirection.MOVE_DOWN
            moved = True
        if not moved:
            move_direction = MoveDirection.MOVE_DOWN

        # clamp vertical
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > HEIGHT:
            player_rect.bottom = HEIGHT

        # room transition
        req = room.get("required_state")
        can_advance = (req is None or state.get(
            req) or state.get(f"{req}") == True)

        # BUG FIX: check required game state flags by string
        state_flags = {
            "room_0_intro_done":       state.get("room_0_intro_done", False),
            "lumi_room_done":          state.get("lumi_room_done", False),
            "postfight_dialogue_done": state.get("postfight_dialogue_done", False),
            "running_done":            state.get("_running_done", False),
            "lala_joined":             state["lala_joined"],
            "scorpion_dead":           state["scorpion_ever_killed"],
            "lulu_joined":             state["lulu_joined"],
            "raft_crossed":            state["raft_crossed"],
            "victory":                 (gs == "victory"),
            None:                      True,
        }
        can_advance = state_flags.get(req, False)

        if player_rect.left >= WIDTH:
            if state["current_room"] < len(ROOMS) - 1:
                if can_advance:
                    enter_room(
                        state, state["current_room"] + 1, from_right=False)
                else:
                    player_rect.right = WIDTH - 1
                    notify("Complete the current quest first!")
            else:
                player_rect.right = WIDTH - 1

        if player_rect.right <= 0:
            if state["current_room"] > 0:
                enter_room(state, state["current_room"] - 1, from_right=True)
            else:
                player_rect.left = 0

        # ── axe cooldown ─────────────────────
        if state["axe_timer"] > 0:
            state["axe_timer"] -= 1

        # ── enchant timer ────────────────────
        if state["axe_enchanted"]:
            state["axe_enchant_timer"] -= 1
            if state["axe_enchant_timer"] <= 0:
                state["axe_enchanted"] = False
                notify("Axe enchant wore off.")

        # ── invulnerability ──────────────────
        if state["player_invulnerable"]:
            state["invuln_timer"] -= 1
            if state["invuln_timer"] <= 0:
                state["player_invulnerable"] = False

        # ── water / breathing ────────────────
        state["in_water"] = any(player_rect.colliderect(wr)
                                for wr in state["water_rects"])
        on_raft = any(player_rect.colliderect(
            r["rect"]) for r in state["raft_objects"])
        if state["in_water"] and not on_raft:
            state["breath"] -= 1
            if state["breath"] <= 0:
                state["player_lives"] = max(0, state["player_lives"] - 1)
                state["breath"] = 60  # brief grace period
        else:
            state["breath"] = min(state["breath"] + 2, BREATH_MAX)

        # move raft if player stands on it
        for r in state["raft_objects"]:
            if player_rect.colliderect(r["rect"]):
                if keys_held[pygame.K_RIGHT] or keys_held[pygame.K_d]:
                    r["rect"].x = min(
                        WIDTH - r["rect"].width, r["rect"].x + spd)
                if keys_held[pygame.K_LEFT] or keys_held[pygame.K_a]:
                    r["rect"].x = max(0, r["rect"].x - spd)
                if keys_held[pygame.K_UP] or keys_held[pygame.K_w]:
                    if r["rect"].top > 0:
                        r["rect"].y = max(0, r["rect"].y - spd)
                if keys_held[pygame.K_DOWN] or keys_held[pygame.K_s]:
                    r["rect"].y = min(
                        HEIGHT - r["rect"].height, r["rect"].y + spd)
                # check if raft crossed the water (reached right side of screen in room 6)
                if state["current_room"] == 6 and r["rect"].right >= WIDTH - 30:
                    state["raft_crossed"] = True
                    notify("You crossed the water!")
                    if state["quest_index"] == 9:
                        state["quest_index"] = 10
                # also allow crossing the boss room water strip (room 7)
                if state["current_room"] == 7 and r["rect"].right >= 700:
                    state["boss_water_crossed"] = True

        # ── scorpion AI ──────────────────────
        if state["scorpion_active"]:
            # Scorpion tracks player slowly
            sx, sy = state["scorpion_rect"].center
            px, py = player_rect.center
            dx, dy = px - sx, py - sy
            dist = math.hypot(dx, dy) or 1
            state["scorpion_rect"].x += int(dx / dist * 1.5)
            state["scorpion_rect"].y += int(dy / dist * 1.5)
            # poison shots
            if random.random() < POISON_CHANCE:
                vx = (dx / dist) * POISON_SPEED
                vy = (dy / dist) * POISON_SPEED
                state["poison_spews"].append({
                    "x": sx, "y": sy, "vx": vx, "vy": vy,
                    "rect": poison_img.get_rect(center=(int(sx), int(sy)))
                })

        # ── lala slime attack ────────────────
        if state["lala_alive"]:
            state["slime_timer"] -= 1
            if state["slime_timer"] <= 0:
                state["slime_timer"] = random.randint(
                    SLIME_MIN_CD, SLIME_MAX_CD)
                # Determine target and flag
                tx, ty, flag = None, None, None
                if state["scorpion_active"]:
                    tx, ty = state["scorpion_rect"].center
                    flag = "scorpion"
                elif state["player_trusts_lala"] != True:
                    tx, ty = player_rect.center
                    flag = "player"
                # else: friendly lala, don't shoot
                if tx is not None:
                    lx, ly = state["lala_rect"].center
                    dx, dy = tx - lx, ty - ly
                    dist = math.hypot(dx, dy) or 1
                    vx, vy = dx / dist * SLIME_SPEED, dy / dist * SLIME_SPEED
                    state["lala_slimes"].append({
                        "x": lx, "y": ly, "vx": vx, "vy": vy,
                        "rect": lala_slime_img.get_rect(center=(int(lx), int(ly))),
                        "target": flag, "age": 0,
                    })

        # ── boss fight AI ────────────────────
        if gs == "boss_fight":
            update_pawbert(state)
            update_boss_lalas(state)
            # Count alive enemies - give bonus notifications
            alive_enemies = sum(1 for bl in state.get(
                "boss_lala_list", []) if bl["alive"])
            alive_allies = sum(1 for al in state.get(
                "ally_lala_list", []) if al["alive"])
            if alive_enemies == 0 and state["pawbert_active"]:
                notify("All enemy LaLas defeated! Focus on Pawbert!")

        # ── projectile updates ───────────────

        # knives
        for k in state["knives"][:]:
            k["rect"].x += k["vx"]
            if k["rect"].right < 0 or k["rect"].left > WIDTH:
                state["knives"].remove(k)
                continue
            if state["lala_alive"] and k["rect"].colliderect(state["lala_rect"]):
                if state["current_room"] == 2:
                    state["lala_lives"] = max(1, state["lala_lives"] - 1)
                    if state["lala_lives"] <= 1:
                        _trigger_lala_surrender(state)
                elif state["current_room"] == 5:
                    notify("They're on your side!")  # can't hurt forest LaLas
                else:
                    state["lala_lives"] = max(0, state["lala_lives"] - 1)
                    if state["lala_lives"] <= 0:
                        state["lala_alive"] = False
                        play_sfx(SFX_ENEMY_WIN)
                state["knives"].remove(k)
                continue
            if state["scorpion_active"] and k["rect"].colliderect(state["scorpion_rect"]):
                state["scorpion_lives"] = max(0, state["scorpion_lives"] - 1)
                if state["scorpion_lives"] <= 0:
                    state["scorpion_active"] = False
                    state["scorpion_ever_killed"] = True
                    play_sfx(SFX_ENEMY_WIN)
                state["knives"].remove(k)
                continue
            if state["pawbert_active"] and k["rect"].colliderect(state["pawbert_rect"]):
                state["pawbert_lives"] = max(0, state["pawbert_lives"] - 1)
                if state["pawbert_lives"] <= 0:
                    state["pawbert_active"] = False
                    play_sfx(SFX_ENEMY_WIN)
                    state["game_state"] = "final_dialogue"
                    state["dialogue_index"] = 0
                    state["quest_index"] = max(state["quest_index"], 12)
                state["knives"].remove(k)
                continue

        # spikes
        for s in state["spikes"][:]:
            s["rect"].x += s["vx"]
            if s["rect"].right < 0 or s["rect"].left > WIDTH:
                state["spikes"].remove(s)
                continue
            if state["scorpion_active"] and s["rect"].colliderect(state["scorpion_rect"]):
                state["scorpion_lives"] = max(0, state["scorpion_lives"] - 1)
                if state["scorpion_lives"] <= 0:
                    state["scorpion_active"] = False
                    state["scorpion_ever_killed"] = True
                    play_sfx(SFX_ENEMY_WIN)
                state["spikes"].remove(s)
                continue

        # poison spews (from scorpion)
        for p in state["poison_spews"][:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["rect"].topleft = (int(p["x"]), int(p["y"]))
            if p["rect"].right < 0 or p["rect"].left > WIDTH or p["rect"].top > HEIGHT:
                state["poison_spews"].remove(p)
                continue
            if not state["player_invulnerable"] and p["rect"].colliderect(player_rect):
                state["player_lives"] = max(0, state["player_lives"] - 1)
                play_sfx(SFX_HIT_DAMAGE)
                state["player_invulnerable"] = True
                state["invuln_timer"] = INVULN_FRAMES
                state["poison_spews"].remove(p)
                continue

        # lala slimes
        for sl in state["lala_slimes"][:]:
            sl["x"] += sl["vx"]
            sl["y"] += sl["vy"]
            sl["age"] += 1
            sl["rect"].topleft = (int(sl["x"]), int(sl["y"]))
            if (sl["rect"].right < 0 or sl["rect"].left > WIDTH
                    or sl["rect"].bottom < 0 or sl["rect"].top > HEIGHT):
                try:
                    state["lala_slimes"].remove(sl)
                except ValueError:
                    pass
                continue
            if (sl.get("target") == "scorpion" and state["scorpion_active"]
                    and sl["rect"].colliderect(state["scorpion_rect"])):
                state["scorpion_lives"] = max(0, state["scorpion_lives"] - 1)
                if state["scorpion_lives"] <= 0:
                    state["scorpion_active"] = False
                    state["scorpion_ever_killed"] = True
                try:
                    state["lala_slimes"].remove(sl)
                except ValueError:
                    pass
                continue
            if sl.get("target") == "player" and sl["rect"].colliderect(player_rect):
                play_sfx(SFX_SLIME)
                if not state["player_invulnerable"]:
                    state["player_lives"] = max(
                        0, state["player_lives"] - SLIME_DMG)
                    play_sfx(SFX_HIT_DAMAGE)
                    state["player_invulnerable"] = True
                    state["invuln_timer"] = INVULN_FRAMES
                try:
                    state["lala_slimes"].remove(sl)
                except ValueError:
                    pass
                continue

        # ── check postfight trigger ──────────
        # BUG FIX: was "== True" (comparison not assignment)
        if (state["lala_alive"] and state["lala_lives"] <= 1
                and not state["postfight_done"]
                and state["current_room"] == 2):
            state["lala_alive"] = False
            state["game_state"] = "postfight_dialogue"
            state["dialogue_index"] = 0
            state["space_released"] = True
            state["first_fight_done"] = True
            state["quest_index"] = 3   # follow LaLa

        # ── death check ──────────────────────
        if state["player_lives"] <= 0 and gs not in ("death", "victory"):
            state["game_state"] = "death"
            state["death_count"] = state.get("death_count", 0) + 1
            dc = state["death_count"]
            if dc == 1:
                play_sfx(SFX_DEATH_1)
            elif dc == 2:
                play_sfx(SFX_DEATH_2)
            else:
                play_sfx(SFX_DEATH_3PLUS)

    # ════════════════════════════════════════
    #  RENDERING
    # ════════════════════════════════════════
    gs = state["game_state"]

    # ── START SCREEN ────────────────────────
    if gs == "start_screen":
        t_ms = pygame.time.get_ticks()
        # Draw bg.jpg with slight darkening overlay
        screen.blit(start_bg, (0, 0))
        dark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 110))
        screen.blit(dark, (0, 0))

        # Starry particles on top
        for i in range(50):
            sx = (i * 317 + t_ms // 20) % WIDTH
            sy = (i * 197) % (HEIGHT - 200)
            brightness = int(160 + 95 * math.sin(t_ms / 500 + i))
            pygame.draw.circle(
                screen, (brightness, brightness, brightness), (sx, sy), 1 + (i % 2))

        # Animated LaLas bouncing
        for i, offset in enumerate([-200, 0, 200]):
            phase = t_ms / 400 + i * 2.1
            bx = WIDTH // 2 + offset
            by = HEIGHT // 2 + 30 + math.sin(phase) * 16
            screen.blit(lala_img, (bx - lala_img.get_width() // 2, int(by)))

        # Title with glow effect
        glow_color = (int(200 + 55*math.sin(t_ms/800)),
                      int(150 + 70*math.sin(t_ms/800+1)), 30)
        ts = title_font.render("Save the LaLas!", True, (255, 220, 80))
        ts_g = title_font.render("Save the LaLas!", True, glow_color)
        ts_s = title_font.render("Save the LaLas!", True, (80, 40, 0))
        screen.blit(ts_s, (WIDTH // 2 - ts.get_width() //
                    2 + 4, HEIGHT // 4 - 36))
        screen.blit(ts_g, (WIDTH // 2 - ts.get_width() //
                    2 + 1, HEIGHT // 4 - 41))
        screen.blit(ts,   (WIDTH // 2 - ts.get_width() //
                    2,     HEIGHT // 4 - 42))

        sub = instr_font.render(
            "An adventure to rescue Lumi!", True, (200, 230, 255))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 4 + 40))

        blink = int(t_ms / 500) % 2 == 0
        if blink:
            is_ = instr_font.render(
                "Press ENTER or SPACE to start", True, (255, 230, 100))
            screen.blit(
                is_, (WIDTH // 2 - is_.get_width() // 2, HEIGHT * 3 // 4))
        pygame.display.flip()
        continue

    # ── NAME INPUT ──────────────────────────
    if gs == "name_input":
        screen.fill((30, 25, 20))
        nh = title_font.render("What's your name?", True, (255, 220, 80))
        screen.blit(nh, (WIDTH // 2 - nh.get_width() // 2, HEIGHT // 3))
        name_buf = state.get("_name_buf", "")
        nd = instr_font.render(name_buf + "|", True, (200, 220, 255))
        pygame.draw.rect(screen, (40, 35, 30),
                         (WIDTH // 2 - 200, HEIGHT // 2 - 20, 400, 50))
        pygame.draw.rect(screen, (172, 147, 98),
                         (WIDTH // 2 - 200, HEIGHT // 2 - 20, 400, 50), 2)
        screen.blit(nd, (WIDTH // 2 - nd.get_width() // 2, HEIGHT // 2 - 10))
        hint = font.render("Press ENTER to confirm", True, (140, 140, 120))
        screen.blit(
            hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 60))
        pygame.display.flip()
        continue

    # ── DEATH ───────────────────────────────
    if gs == "death":
        SKIP == True
        t_ms = pygame.time.get_ticks()
        screen.fill((20, 10, 10))
        # Subtle red pulse
        pulse = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        alpha = int(30 + 20 * math.sin(t_ms / 400))
        pulse.fill((180, 0, 0, alpha))
        screen.blit(pulse, (0, 0))

        ds = title_font.render("You Died.", True, (220, 50, 50))
        ds_s = title_font.render("You Died.", True, (80, 10, 10))
        screen.blit(ds_s, (WIDTH // 2 - ds.get_width() //
                    2 + 3, HEIGHT // 3 + 3))
        screen.blit(ds, (WIDTH // 2 - ds.get_width() // 2, HEIGHT // 3))
        rs = instr_font.render(
            "Press ENTER or SPACE to try again", True, (200, 160, 160))
        screen.blit(rs, (WIDTH // 2 - rs.get_width() // 2, HEIGHT // 3 + 90))
        tip = small_font.render(
            "Tip: Eat cactus fruit (F) to heal!", True, (160, 120, 120))
        screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, HEIGHT // 3 + 140))
        pygame.display.flip()
        continue

    # ── VICTORY ─────────────────────────────
    if gs == "victory":
        t_ms = pygame.time.get_ticks()
        screen.fill((10, 30, 15))
        # Draw meadow bg faded
        faded = meadow_bg.copy()
        faded.set_alpha(120)
        screen.blit(faded, (0, 0))
        draw_confetti(screen)

        # Player and Lumi reunion
        player_vic_x = WIDTH // 2 - 110
        lumi_vic_x = WIDTH // 2 + 30
        ground_y = HEIGHT - 200
        bob = math.sin(t_ms / 400) * 8
        screen.blit(player, (player_vic_x, ground_y -
                    player_rect.height + bob))
        screen.blit(lumi_img, (lumi_vic_x, ground_y -
                    lumi_img.get_height() + bob * -1))
        # LaLas celebrating
        for i, loff in enumerate([-320, -220, 280, 380]):
            phase = t_ms / 350 + i * 1.5
            screen.blit(lala_img, (WIDTH // 2 + loff, ground_y -
                        lala_img.get_height() + math.sin(phase) * 20))

        # Dark overlay at top for text
        overlay = pygame.Surface((WIDTH, HEIGHT // 2), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        glow = int(200 + 55*math.sin(t_ms/600))
        vs = title_font.render("YOU WON! ⭐", True, (255, glow, 50))
        ws = instr_font.render(
            f"You saved Lumi and all the LaLas!", True, (200, 255, 180))
        rs = font.render("Press ENTER or SPACE to play again",
                         True, (180, 180, 160))
        screen.blit(vs, (WIDTH // 2 - vs.get_width() // 2, 60))
        screen.blit(ws, (WIDTH // 2 - ws.get_width() // 2, 150))
        screen.blit(rs, (WIDTH // 2 - rs.get_width() // 2, 200))
        pygame.display.flip()
        continue

    # ── INTRO DIALOGUE ──────────────────────
    if gs == "intro":
        screen.blit(room["bg"], (0, 0))
        # No lala in the player's room - player is alone
        screen.blit(player, player_rect)
        idx = state["dialogue_index"]
        if idx < len(INTRO_DIALOGUE):
            sp, txt = INTRO_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── LUMI'S ROOM DIALOGUE ────────────────
    if gs == "lumi_room_dialogue":
        screen.blit(room2_bg, (0, 0))
        screen.blit(player, player_rect)
        idx = state["dialogue_index"]
        if idx < len(LUMI_ROOM_DIALOGUE):
            sp, txt = LUMI_ROOM_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── KITCHEN DIALOGUE ────────────────────
    if gs == "kitchen_dialogue":
        screen.blit(kitchen_bg, (0, 0))
        screen.blit(player, player_rect)
        screen.blit(lala_img, (700, 500))
        idx = state["dialogue_index"]
        if idx < len(KITCHEN_DIALOGUE):
            sp, txt = KITCHEN_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── POSTFIGHT DIALOGUE ───────────────────
    if gs == "postfight_dialogue":
        screen.blit(room["bg"], (0, 0))
        screen.blit(lala_img, state["lala_rect"])
        screen.blit(player, player_rect)
        idx = state["dialogue_index"]
        if idx < len(POSTFIGHT_DIALOGUE):
            sp, txt = POSTFIGHT_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── DIALOGUE CHOICE ──────────────────────
    if gs == "dialogue_choice":
        screen.blit(room["bg"], (0, 0))
        screen.blit(player, player_rect)
        if state["lala_alive"] or state.get("postfight_done"):
            screen.blit(lala_img, state["lala_rect"])
        render_dialogue_panel(screen, "Choose:", "What will you do?",
                              choices=state["dialogue_choices"],
                              selected=state["selected_choice"])
        pygame.display.flip()
        continue

    # ── RUNNING SEQUENCE ─────────────────────
    if gs == "running_sequence" and running_seq:
        running_seq.update()
        running_seq.draw(screen)
        sp, txt = running_seq.current() if not running_seq.done else (
            SP_NARR, "Press SPACE to continue...")
        txt_replaced = txt.replace("{name}", state["player_name"])
        render_dialogue_panel(screen, sp, txt_replaced)
        pygame.display.flip()
        continue

    # ── DESERT DIALOGUE ──────────────────────
    if gs == "desert_dialogue":
        screen.blit(desert_bg, (0, 0))
        screen.blit(player, player_rect)
        screen.blit(lala_img, state["lala_rect"])
        idx = state["dialogue_index"]
        if idx < len(DESERT_DIALOGUE):
            sp, txt = DESERT_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── FOREST DIALOGUE ──────────────────────
    if gs in ("forest_dialogue", "forest_dialogue_2"):
        screen.blit(forest_bg, (0, 0))
        screen.blit(player, player_rect)
        screen.blit(lala_img, state["lala_rect"])
        if state["lulu_rect"]:
            screen.blit(lulu_img, state["lulu_rect"])
        # Draw 10 LaLas scattered behind LuLu to show the group
        lala_crowd_positions = [
            (620, 500), (680, 480), (740, 510), (800, 490), (860, 510),
            (640, 560), (700, 545), (760, 560), (820, 550), (880, 555),
        ]
        for lp in lala_crowd_positions:
            screen.blit(lala_img, lp)
        dlg = LULU_DIALOGUE_1 if gs == "forest_dialogue" else LULU_DIALOGUE_2
        idx = state["dialogue_index"]
        if idx < len(dlg):
            sp, txt = dlg[idx]
            txt = txt.replace("{name}", state["player_name"])
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── SHORE DIALOGUE ───────────────────────
    if gs == "shore_dialogue":
        screen.blit(shore_bg, (0, 0))
        screen.blit(player, player_rect)
        screen.blit(lala_img, state["lala_rect"])
        idx = state["dialogue_index"]
        if idx < len(SHORE_DIALOGUE):
            sp, txt = SHORE_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── BOSS DIALOGUE ────────────────────────
    if gs == "boss_dialogue":
        screen.blit(ROOMS[7]["bg"], (0, 0))
        screen.blit(player, player_rect)
        screen.blit(lala_img, state["lala_rect"])
        draw_boss_lalas(screen, state.get("boss_lala_list"))
        idx = state["dialogue_index"]
        if idx < len(BOSS_DIALOGUE):
            sp, txt = BOSS_DIALOGUE[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ── FINAL DIALOGUE ───────────────────────
    if gs == "final_dialogue":
        screen.blit(room2_bg, (0, 0))  # Use Lumi's room bg for the reunion
        screen.blit(player, player_rect)
        # Lumi stands at the right side (by the window)
        lumi_x = WIDTH - lumi_img.get_width() - 80
        lumi_y = HEIGHT - lumi_img.get_height() - 60
        screen.blit(lumi_img, (lumi_x, lumi_y))
        txt_list = [(sp, t.replace("{name}", state["player_name"]))
                    for sp, t in FINAL_DIALOGUE]
        idx = state["dialogue_index"]
        if idx < len(txt_list):
            sp, txt = txt_list[idx]
            render_dialogue_panel(screen, sp, txt)
        pygame.display.flip()
        continue

    # ════════════════════════════════════════
    #  MAIN GAME RENDER
    # ════════════════════════════════════════
    # background already drawn at top of loop

    # water zones
    for wr in state["water_rects"]:
        water_surf = pygame.Surface((wr.w, wr.h), pygame.SRCALPHA)
        water_surf.fill((40, 100, 200, 180))
        screen.blit(water_surf, wr.topleft)

    # raft objects
    for r in state["raft_objects"]:
        pygame.draw.rect(screen, (120, 70, 30), r["rect"])
        screen.blit(plank_img, r["rect"].topleft)

    # trees
    for t in state["trees"]:
        if t.get("img"):
            screen.blit(t["img"], t["rect"])
            # health bar on tree
            hw = t["rect"].width
            hh = 4
            pygame.draw.rect(screen, (60, 60, 60),
                             (t["rect"].x, t["rect"].y - 8, hw, hh))
            pygame.draw.rect(screen, (100, 200, 60),
                             (t["rect"].x, t["rect"].y - 8, int(hw * t["health"] / 3), hh))

    # dropped items
    for item in state["dropped_items"]:
        screen.blit(item["img"], item["rect"])
        # glow/outline so items are visible
        pygame.draw.rect(screen, (255, 220, 60), item["rect"].inflate(4, 4), 1)

    # lala (enemy or ally)
    if state["lala_alive"]:
        screen.blit(lala_img, state["lala_rect"])
        draw_hp_bar(screen, state["lala_rect"].x, state["lala_rect"].y - 12,
                    state["lala_lives"], ROOMS[state["current_room"]].get(
                        "lala_lives", 3),
                    w=lala_img.get_width(), color=(180, 80, 220))

    # lulu
    if state["lulu_alive"] and state["lulu_rect"]:
        screen.blit(lulu_img, state["lulu_rect"])
        draw_hp_bar(screen, state["lulu_rect"].x, state["lulu_rect"].y - 12,
                    state["lulu_lives"], 4,
                    w=lulu_img.get_width(), color=(80, 200, 220))

    # scorpion
    if state["scorpion_active"]:
        screen.blit(scorpion_img, state["scorpion_rect"])
        draw_hp_bar(screen, state["scorpion_rect"].x, state["scorpion_rect"].y - 14,
                    state["scorpion_lives"], ROOMS[state["current_room"]].get(
                        "scorpion_lives", 5),
                    w=scorpion_img.get_width(), color=(200, 80, 50))

    # Pawbert boss
    if state["pawbert_active"]:
        pr = state["pawbert_rect"]
        t_ms2 = pygame.time.get_ticks()
        shake = int(math.sin(t_ms2 / 60) *
                    4) if state["pawbert_lives"] <= PAWBERT_MAX_LIVES // 3 else 0
        screen.blit(pawbert_img, (pr.x + shake, pr.y))
        draw_hp_bar(screen, WIDTH // 2 - 150, 62,
                    state["pawbert_lives"], PAWBERT_MAX_LIVES,
                    w=300, h=22, color=(220, 40, 40))
        bname = instr_font.render("⚡ Mr. Pawbert ⚡", True, (255, 80, 80))
        screen.blit(bname, (WIDTH // 2 - bname.get_width() // 2, 34))

    # boss lalas (enemy side)
    if gs == "boss_fight" and state.get("boss_lalas_active"):
        draw_boss_lalas(screen, state.get("boss_lala_list"))
        draw_ally_lalas(screen, state.get("ally_lala_list", []))
        # Battle counter HUD
        alive_e = sum(1 for bl in state.get(
            "boss_lala_list", []) if bl["alive"])
        alive_a = sum(1 for al in state.get(
            "ally_lala_list", []) if al["alive"])
        e_txt = small_font.render(
            f"Enemy LaLas: {alive_e}", True, (220, 80, 80))
        a_txt = small_font.render(
            f"Your LaLas:  {alive_a}", True, (80, 220, 120))
        screen.blit(e_txt, (WIDTH - 180, 90))
        screen.blit(a_txt, (WIDTH - 180, 110))

    # player (flashing when invulnerable)
    if not state["player_invulnerable"] or (state["invuln_timer"] // 6) % 2 == 0:
        screen.blit(player, player_rect)

    # projectiles
    for k in state["knives"]:
        screen.blit(knife_img, k["rect"])
    for s in state["spikes"]:
        screen.blit(spike_img, s["rect"])
    for p in state["poison_spews"]:
        screen.blit(poison_img, p["rect"])

    for sl in state["lala_slimes"]:
        screen.blit(lala_slime_img, sl["rect"])

    # breath bar (if in water without raft)
    if state["in_water"] and not any(player_rect.colliderect(r["rect"]) for r in state["raft_objects"]):
        bw, bh = 160, 12
        bx, by = WIDTH // 2 - bw // 2, 52
        pygame.draw.rect(screen, (30, 30, 60), (bx, by, bw, bh))
        ratio = max(0, state["breath"] / BREATH_MAX)
        col = (50, 150, 230) if ratio > 0.3 else (220, 50, 50)
        pygame.draw.rect(screen, col, (bx, by, int(bw * ratio), bh))
        bl = small_font.render("BREATH", True, (200, 200, 255))
        screen.blit(bl, (bx + bw + 6, by))

    # enchant/poison HUD + player glow when enchanted
    if state["axe_enchanted"]:
        t_ms4 = pygame.time.get_ticks()
        glow_a = int(80 + 60 * math.sin(t_ms4 / 200))
        glow_s = pygame.Surface(
            (player_rect.w + 20, player_rect.h + 20), pygame.SRCALPHA)
        glow_s.fill((0, 230, 200, glow_a))
        screen.blit(glow_s, (player_rect.x - 10, player_rect.y - 10))
        es = font.render(
            f"⚡ Axe Enchanted  {state['axe_enchant_timer'] // 60}s", True, (0, 230, 200))
        screen.blit(es, (10, HEIGHT - 110))

    # HP hearts (filled = alive, dimmed = lost)
    draw_hearts(screen, state["player_lives"], state["max_player_lives"])
    pn = font.render(state["player_name"], True, (220, 210, 180))
    screen.blit(pn, (10, 10 + heart_img.get_height() + 4))

    # inventory
    render_inventory(screen, mouse_pos,
                     state["inventory"], state["equipped_index"])

    # crafting panel
    if state["is_crafting_open"]:
        display_crafting_panel(screen, state["inventory"],
                               state["axe_enchanted"], state["axe_enchant_timer"])

    # raft crafting mini-game
    if state["raft_crafting"]:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        area = get_raft_area_rect()
        pygame.draw.rect(screen, (200, 195, 170), area)
        pygame.draw.rect(screen, (100, 90, 70), area, 3)
        rt = instr_font.render(
            "Raft Crafting  — Q/E rotate  T tie  Esc cancel", True, (20, 20, 20))
        screen.blit(rt, (area.x + 10, area.y + 8))
        for pl in state["placed_planks"]:
            img = pygame.transform.rotate(plank_img, pl.get("angle", 0))
            ir = img.get_rect(center=pl["rect"].center)
            screen.blit(img, ir)
            col = (30, 160, 30) if pl is state["selected_plank"] else (
                80, 50, 20)
            pygame.draw.rect(screen, col, ir, 2)
        for snap_pt in get_snap_cells():
            pygame.draw.circle(screen, (150, 150, 150), snap_pt, 5, 1)
        for p in state["raft_palette"]:
            ir = plank_img.get_rect(center=p["rect"].center)
            screen.blit(plank_img, ir)
            pygame.draw.rect(screen, (120, 120, 120)
                             if p["used"] else (30, 160, 30), p["rect"], 3)
        # ── Raft crafting resource panel ──
        planks_placed = len(state["placed_planks"])
        resin_count = count_item(state["inventory"], ITEM_RESIN)
        res_panel_x = area.x
        res_panel_y = area.bottom + 10
        pygame.draw.rect(screen, (40, 35, 28),
                         (res_panel_x, res_panel_y, 420, 70))
        pygame.draw.rect(screen, (140, 110, 60),
                         (res_panel_x, res_panel_y, 420, 70), 2)
        # Wood plank progress
        plank_col = (60, 200, 60) if planks_placed >= WOOD_FOR_RAFT else (
            220, 160, 60)
        wood_txt = instr_font.render(
            f"Planks: {planks_placed}/{WOOD_FOR_RAFT}", True, plank_col)
        screen.blit(wood_inv_img, (res_panel_x + 10, res_panel_y + 18))
        screen.blit(wood_txt, (res_panel_x + 50, res_panel_y + 22))
        # Resin counter
        resin_col = (60, 200, 60) if resin_count >= RESIN_TO_TIE else (
            220, 80, 80)
        resin_txt = instr_font.render(
            f"Resin: {resin_count}/{RESIN_TO_TIE}", True, resin_col)
        screen.blit(resin_inv_img, (res_panel_x + 220, res_panel_y + 18))
        screen.blit(resin_txt, (res_panel_x + 260, res_panel_y + 22))
        # Tie button hint
        all_ready = planks_placed >= WOOD_FOR_RAFT and resin_count >= RESIN_TO_TIE
        hint_col = (255, 230, 80) if all_ready else (120, 120, 100)
        tie_hint = small_font.render(
            "T = Tie Raft (needs all 4 planks + 1 resin)" if not all_ready else "T = TIE RAFT — READY!", True, hint_col)
        screen.blit(tie_hint, (res_panel_x + 10, res_panel_y + 52))

    # quest log / key guide
    draw_quest(screen, state["quest_index"])
    draw_ui_buttons(screen)
    if state["is_quest_log_open"]:
        draw_quest_log(screen, state["quest_index"])
    if state["is_key_guide_open"]:
        draw_key_guide(screen)

    # notifications
    draw_notifications(screen)

    # minimap (always shown in corner; N key opens full view)
    draw_minimap(screen, state["current_room"], state.get("map_open", False))

    # room name — elegant shadow text, no box, no dots
    rn_shadow = instr_font.render(
        ROOMS[state['current_room']]['name'], True, (20, 15, 10))
    rn = instr_font.render(
        ROOMS[state['current_room']]['name'], True, (255, 230, 130))
    rx = WIDTH // 2 - rn.get_width() // 2
    screen.blit(rn_shadow, (rx + 2, 8))
    screen.blit(rn,        (rx,     6))

    # Room transition flash
    if state.get("room_transition_flash", 0) > 0:
        flash_alpha = min(255, state["room_transition_flash"] * 13)
        flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash_surf.fill((255, 255, 255, flash_alpha))
        screen.blit(flash_surf, (0, 0))
        state["room_transition_flash"] -= 1

    # ── music mini-player ───────────────────
    mp_play_rect, mp_slider_rect, mp_slider_coords = draw_mini_player(screen, mouse_pos)
    pygame.display.flip()

pygame.quit()
sys.exit()
