import pygame
import random
import sys

# Constants
GRID_X_COUNT = 4
GRID_Y_COUNT = 4
PIECE_SIZE = 100
WIDTH = GRID_X_COUNT * PIECE_SIZE
HEIGHT = GRID_Y_COUNT * PIECE_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")

# Initialize grid
def get_initial_value(x, y):
    return y * GRID_X_COUNT + x + 1

def reset():
    global grid
    grid = [[get_initial_value(x, y) for x in range(GRID_X_COUNT)] for y in range(GRID_Y_COUNT)]
    grid[-1][-1] = GRID_X_COUNT * GRID_Y_COUNT  # Set the last cell as empty

    # Shuffle the grid
    for _ in range(1000):
        move(random.choice(('down', 'up', 'right', 'left')))

def is_complete():
    for y in range(GRID_Y_COUNT):
        for x in range(GRID_X_COUNT):
            if grid[y][x] != get_initial_value(x, y) and grid[y][x] != GRID_X_COUNT * GRID_Y_COUNT:
                return False
    return True

def move(direction):
    empty_x, empty_y = [(x, y) for y in range(GRID_Y_COUNT) for x in range(GRID_X_COUNT) if grid[y][x] == GRID_X_COUNT * GRID_Y_COUNT][0]

    new_empty_x, new_empty_y = empty_x, empty_y

    if direction == 'down':
        new_empty_y += 1
    elif direction == 'up':
        new_empty_y -= 1
    elif direction == 'right':
        new_empty_x += 1
    elif direction == 'left':
        new_empty_x -= 1

    if 0 <= new_empty_y < GRID_Y_COUNT and 0 <= new_empty_x < GRID_X_COUNT:
        # Swap the empty tile with the adjacent tile
        grid[empty_y][empty_x], grid[new_empty_y][new_empty_x] = grid[new_empty_y][new_empty_x], grid[empty_y][empty_x]

# Start the game
reset()

def on_key_down(event):
    if event.key == pygame.K_DOWN:
        move('down')
    elif event.key == pygame.K_UP:
        move('up')
    elif event.key == pygame.K_RIGHT:
        move('right')
    elif event.key == pygame.K_LEFT:
        move('left')
    elif event.key == pygame.K_r:
        reset()

    if is_complete():
        reset()

def draw():
    screen.fill((0, 0, 0))

    for y in range(GRID_Y_COUNT):
        for x in range(GRID_X_COUNT):
            if grid[y][x] == GRID_X_COUNT * GRID_Y_COUNT:
                continue

            piece_draw_size = PIECE_SIZE - 1
            pygame.draw.rect(
                screen,
                (100, 20, 150),
                (x * PIECE_SIZE, y * PIECE_SIZE, piece_draw_size, piece_draw_size)
            )

            font = pygame.font.Font(None, 60)
            text = font.render(str(grid[y][x]), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x * PIECE_SIZE + PIECE_SIZE // 2, y * PIECE_SIZE + PIECE_SIZE // 2))
            screen.blit(text, text_rect)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            on_key_down(event)

    draw()
    pygame.display.flip()
