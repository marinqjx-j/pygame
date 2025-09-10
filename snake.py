import os
import sys
import random
import pygame

# Avoid audio device errors in containers
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

# --------------------------
# Config
# --------------------------
CELL = 20
GRID_W, GRID_H = 32, 24               # 32x24 grid -> 640x480 window
WIDTH, HEIGHT = GRID_W * CELL, GRID_H * CELL
MOVE_MS_START = 140                   # initial step interval (ms)
MOVE_MS_MIN = 70                      # fastest speed
SPEEDUP_EVERY = 5                     # speed up every N apples

# Colors
BG = (18, 18, 18)
SNAKE = (80, 220, 120)
SNAKE_HEAD = (120, 255, 160)
FOOD = (240, 80, 80)
GRID = (28, 28, 28)
TEXT = (230, 230, 230)

# Directions as (dx, dy) in grid units
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

# --------------------------
# Helpers
# --------------------------
def wrap(pos):
    """Wrap a (x, y) grid position around the edges."""
    x, y = pos
    return (x % GRID_W, y % GRID_H)

def new_food(snake):
    """Spawn food not on the snake."""
    free = {(x, y) for x in range(GRID_W) for y in range(GRID_H)} - set(snake)
    return random.choice(list(free)) if free else None

def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRID, (0, y), (WIDTH, y))

def draw_rect(surface, color, cell_xy):
    x, y = cell_xy
    pygame.draw.rect(surface, color, (x * CELL, y * CELL, CELL, CELL))

# --------------------------
# Game
# --------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake (Wrap Through Walls)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 56)

    # -------- Initial State (fixed) --------
    cx, cy = GRID_W // 2, GRID_H // 2
    # Head is leftmost; body extends to the right → moving LEFT is safe
    snake = [(cx, cy), (cx + 1, cy), (cx + 2, cy), (cx + 3, cy)]
    direction = LEFT
    queued_direction = LEFT
    food = new_food(snake)
    score = 0
    move_ms = MOVE_MS_START
    paused = False
    dead = False

    MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_EVENT, move_ms)

    def reset():
        nonlocal snake, direction, queued_direction, food, score, move_ms, dead, paused
        cx2, cy2 = GRID_W // 2, GRID_H // 2
        snake = [(cx2, cy2), (cx2 + 1, cy2), (cx2 + 2, cy2), (cx2 + 3, cy2)]
        direction = LEFT
        queued_direction = LEFT
        food = new_food(snake)
        score = 0
        move_ms = MOVE_MS_START
        pygame.time.set_timer(MOVE_EVENT, move_ms)
        dead = False
        paused = False

    while True:
        # ------------- Events -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key in (pygame.K_p, pygame.K_SPACE) and not dead:
                    paused = not paused
                if event.key in (pygame.K_r,):
                    reset()
                # Direction input (ignore 180° reversals)
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != DOWN: queued_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != UP: queued_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != RIGHT: queued_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != LEFT: queued_direction = RIGHT

            if event.type == MOVE_EVENT and not paused and not dead:
                # apply queued direction once per tick
                if queued_direction != OPPOSITE[direction]:
                    direction = queued_direction

                # compute new head with wrap
                hx, hy = snake[0]
                dx, dy = direction
                new_head = wrap((hx + dx, hy + dy))

                # self-collision ends game
                if new_head in snake:
                    dead = True
                else:
                    snake.insert(0, new_head)
                    if food and new_head == food:
                        score += 1
                        food = new_food(snake)
                        # speed up every few apples
                        if score % SPEEDUP_EVERY == 0 and move_ms > MOVE_MS_MIN:
                            move_ms = max(MOVE_MS_MIN, move_ms - 10)
                            pygame.time.set_timer(MOVE_EVENT, move_ms)
                    else:
                        snake.pop()  # move forward (no growth)

        # ------------- Draw -------------
        screen.fill(BG)
        draw_grid(screen)

        if food:
            draw_rect(screen, FOOD, food)

        # snake
        if snake:
            draw_rect(screen, SNAKE_HEAD, snake[0])
            for seg in snake[1:]:
                draw_rect(screen, SNAKE, seg)

        # HUD
        steps_per_sec = round(1000 / max(move_ms, 1), 1)
        hud = font.render(f"Score: {score}   Speed: {steps_per_sec} steps/s", True, TEXT)
        screen.blit(hud, (10, 8))

        if paused and not dead:
            t = big_font.render("PAUSED", True, TEXT)
            screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2)))
            s = font.render("Press SPACE/P to resume", True, TEXT)
            screen.blit(s, s.get_rect(center=(WIDTH//2, HEIGHT//2 + 36)))

        if dead:
            t = big_font.render("GAME OVER", True, TEXT)
            screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2 - 10)))
            s = font.render("Press R to restart", True, TEXT)
            screen.blit(s, s.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))

        pygame.display.flip()
        clock.tick(120)  # redraw cap; movement is timer-based

if __name__ == "__main__":
    main()
