import pygame
import random
import sys

# Constants
bird_x = 62
bird_width = 30
bird_height = 25

playing_area_width = 300
playing_area_height = 388

pipe_space_height = 100
pipe_width = 54

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((playing_area_width, playing_area_height))
pygame.display.set_caption("Flappy Bird Clone")

# Game Variables
bird_y = 200
bird_y_speed = 0
score = 0
upcoming_pipe = 1

# Pipe positions
pipe_1_x = playing_area_width
pipe_1_space_y = 0
pipe_2_x = playing_area_width + ((playing_area_width + pipe_width) / 2)
pipe_2_space_y = 0

def new_pipe_space_y():
    pipe_space_y_min = 54
    pipe_space_y = random.randint(
        pipe_space_y_min,
        playing_area_height - pipe_space_height - pipe_space_y_min
    )
    return pipe_space_y

def reset():
    global bird_y, bird_y_speed, pipe_1_x, pipe_1_space_y, pipe_2_x, pipe_2_space_y, score, upcoming_pipe

    bird_y = 200
    bird_y_speed = 0

    pipe_1_x = playing_area_width
    pipe_1_space_y = new_pipe_space_y()

    pipe_2_x = playing_area_width + ((playing_area_width + pipe_width) / 2)
    pipe_2_space_y = new_pipe_space_y()

    score = 0
    upcoming_pipe = 1

reset()

def update(dt):
    global bird_y, bird_y_speed, pipe_1_x, pipe_2_x, pipe_1_space_y, pipe_2_space_y, score, upcoming_pipe

    bird_y_speed += 516 * dt
    bird_y += bird_y_speed * dt

    def move_pipe(pipe_x, pipe_space_y):
        pipe_x -= 60 * dt

        if (pipe_x + pipe_width) < 0:
            pipe_x = playing_area_width
            pipe_space_y = new_pipe_space_y()

        return pipe_x, pipe_space_y

    pipe_1_x, pipe_1_space_y = move_pipe(pipe_1_x, pipe_1_space_y)
    pipe_2_x, pipe_2_space_y = move_pipe(pipe_2_x, pipe_2_space_y)

    def is_bird_colliding_with_pipe(pipe_x, pipe_space_y):
        return (
            bird_x < (pipe_x + pipe_width)
            and (bird_x + bird_width) > pipe_x
            and (
                bird_y < pipe_space_y
                or (bird_y + bird_height) > (pipe_space_y + pipe_space_height)
            )
        )

    if (
        is_bird_colliding_with_pipe(pipe_1_x, pipe_1_space_y)
        or is_bird_colliding_with_pipe(pipe_2_x, pipe_2_space_y)
        or bird_y > playing_area_height
    ):
        reset()

    def update_score_and_closest_pipe(this_pipe, pipe_x, other_pipe):
        global score, upcoming_pipe

        if (
            upcoming_pipe == this_pipe
            and bird_x > (pipe_x + pipe_width)
        ):
            score += 1
            upcoming_pipe = other_pipe

    update_score_and_closest_pipe(1, pipe_1_x, 2)
    update_score_and_closest_pipe(2, pipe_2_x, 1)

def on_key_down():
    global bird_y_speed

    if bird_y > 0:
        bird_y_speed = -165

def draw():
    screen.fill((0, 0, 0))

    # Draw playing area background
    pygame.draw.rect(screen, (35, 92, 118), (0, 0, playing_area_width, playing_area_height))

    # Draw bird
    pygame.draw.rect(screen, (224, 214, 68), (bird_x, bird_y, bird_width, bird_height))

    def draw_pipe(pipe_x, pipe_space_y):
        # Draw upper pipe
        pygame.draw.rect(screen, (94, 201, 72), (pipe_x, 0, pipe_width, pipe_space_y))
        # Draw lower pipe
        pygame.draw.rect(screen, (94, 201, 72), (pipe_x, pipe_space_y + pipe_space_height, pipe_width, playing_area_height - pipe_space_y - pipe_space_height))

    draw_pipe(pipe_1_x, pipe_1_space_y)
    draw_pipe(pipe_2_x, pipe_2_space_y)

    # Draw score
    font = pygame.font.Font(None, 36)
    text_surface = font.render(str(score), True, (255, 255, 255))
    screen.blit(text_surface, (15, 15))

# Main game loop
clock = pygame.time.Clock()
while True:
    dt = clock.tick(60) / 1000.0  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            on_key_down()

    update(dt)
    draw()
    pygame.display.flip()
