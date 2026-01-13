import pygame
pygame.init()
from enum import Enum

width = 1250
height = 770
panel_img = pygame.image.load("panel.png").convert_alpha()
panel_img = pygame.transform.smoothscale(panel_img, (800, 250))
knife_img = pygame.image.load("knife.png").convert_alpha()
spike_img = pygame.image.load("spike.png").convert_alpha()
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (50, 50))
cactusfruit_img = pygame.image.load("cactusfruit.png").convert_alpha()
slot_img = pygame.image.load("slot.png").convert_alpha()
wood_img = pygame.image.load("wood.png").convert_alpha()
stone_img = pygame.image.load("stone.png").convert_alpha()
axe_img = pygame.image.load("axe.png").convert_alpha()
font = pygame.font.SysFont('Times New Roman', 20)

MAX_STACK = 20
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

item_imgs = [knife_inv_img, food_inv_img, spike_inv_img,
             wood_inv_img, stone_inv_img, axe_inv_img]


inventory = [None] * INV_SLOTS
equipped_index = 0

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


