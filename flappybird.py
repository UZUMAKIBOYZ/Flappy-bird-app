import os
import random
import pygame

pygame.init()
pygame.mixer.init()


# Project paths

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# Flappy Bird font

font = pygame.font.Font(
    os.path.join(
        ASSETS_DIR,
        "FlappyBirdy.ttf"
    ),
    55
)


# Screen

WIDTH = 480
HEIGHT = 720

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("Flappy Bird")


# Colors

SKY = (135, 206, 235)


# Load bird assets

bird_frames = [
    pygame.image.load(
        os.path.join(ASSETS_DIR, "birdup.png")
    ).convert_alpha(),

    pygame.image.load(
        os.path.join(ASSETS_DIR, "birdmid.png")
    ).convert_alpha(),

    pygame.image.load(
        os.path.join(ASSETS_DIR, "birddown.png")
    ).convert_alpha()
]


# Load pipe assets

pipe_body = pygame.image.load(
    os.path.join(ASSETS_DIR, "pipe.png")
).convert_alpha()

pipe_cap = pygame.image.load(
    os.path.join(ASSETS_DIR, "pipecap.png")
).convert_alpha()

top_pipe_cap = pygame.transform.flip(
    pipe_cap,
    False,
    True
)


# Load floor

floor_image = pygame.image.load(
    os.path.join(ASSETS_DIR, "floor.png")
).convert_alpha()


# Load game over image

gameover_image = pygame.image.load(
    os.path.join(ASSETS_DIR, "gameover.png")
).convert_alpha()


# Load number sprites

number_images = {}

for number in range(10):

    number_images[number] = pygame.image.load(
        os.path.join(
            ASSETS_DIR,
            str(number) + ".png"
        )
    ).convert_alpha()


# Load sounds

flap_sound = pygame.mixer.Sound(
    os.path.join(
        ASSETS_DIR,
        "swoosh.wav"
    )
)

point_sound = pygame.mixer.Sound(
    os.path.join(
        ASSETS_DIR,
        "point.wav"
    )
)

hit_sound = pygame.mixer.Sound(
    os.path.join(
        ASSETS_DIR,
        "die.wav"
    )
)


# Bird settings

bird_x = 100
bird_y = 300
bird_velocity = 0

gravity = 0.45
flap_strength = -8


# Bird animation

bird_frame = 0
animation_timer = 0
animation_speed = 100


# Pipe settings

pipes = []

PIPE_GAP = 180

PIPE_SPEED_START = 3
PIPE_SPEED = PIPE_SPEED_START

PIPE_SPEED_INCREASE = 0.5

PIPE_DISTANCE = 280

last_gap_center = None


# Score

score = 0
high_score = 0


# Game state

game_over = False
death_sound_played = False


# Reset game

def reset_game():

    global bird_y
    global bird_velocity
    global bird_frame
    global animation_timer
    global pipes
    global last_gap_center
    global game_over
    global death_sound_played
    global score
    global PIPE_SPEED

    bird_y = 300

    bird_velocity = 0

    bird_frame = 0

    animation_timer = 0

    pipes.clear()

    last_gap_center = None

    score = 0

    PIPE_SPEED = PIPE_SPEED_START

    game_over = False

    death_sound_played = False


# Player death

def die():

    global game_over
    global death_sound_played
    global high_score

    if not game_over:

        game_over = True

        if score > high_score:

            high_score = score

        if not death_sound_played:

            hit_sound.play()

            death_sound_played = True


# Draw centered number

def draw_number(
    number,
    center_x,
    y
):

    digits = str(number)

    spacing = 2

    total_width = 0


    # Calculate width

    for digit in digits:

        image = number_images[
            int(digit)
        ]

        total_width += image.get_width()


    total_width += (
        spacing
        * (len(digits) - 1)
    )


    # Starting position

    x = (
        center_x
        - total_width // 2
    )


    # Draw digits

    for digit in digits:

        image = number_images[
            int(digit)
        ]

        screen.blit(
            image,
            (
                x,
                y
            )
        )

        x += (
            image.get_width()
            + spacing
        )


# Draw number from left position

def draw_number_left(
    number,
    x,
    y
):

    digits = str(number)

    spacing = 2

    current_x = x


    for digit in digits:

        image = number_images[
            int(digit)
        ]

        screen.blit(
            image,
            (
                current_x,
                y
            )
        )

        current_x += (
            image.get_width()
            + spacing
        )


# Create pipe

def create_pipe():

    global last_gap_center

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    floor_height = floor_image.get_height()

    playable_height = (
        screen_height
        - floor_height
    )


    # Calculate gap

    gap = min(
        PIPE_GAP,
        playable_height - 160
    )

    margin = 80

    minimum_center = (
        margin
        + gap // 2
    )

    maximum_center = (
        playable_height
        - margin
        - gap // 2
    )


    # Pick gap position

    if maximum_center <= minimum_center:

        gap_center = (
            playable_height // 2
        )

    elif last_gap_center is None:

        gap_center = random.randint(
            minimum_center,
            maximum_center
        )

    else:

        gap_center = (
            last_gap_center
            + random.randint(
                -60,
                60
            )
        )

        gap_center = max(
            minimum_center,
            min(
                maximum_center,
                gap_center
            )
        )


    last_gap_center = gap_center


    # Gap boundaries

    gap_top = (
        gap_center
        - gap // 2
    )

    gap_bottom = (
        gap_center
        + gap // 2
    )


    # Pipe position

    x = screen_width + 40

    cap_height = pipe_cap.get_height()

    body_width = pipe_body.get_width()


    # Top body

    top_body_height = (
        gap_top
        - cap_height
    )


    if top_body_height > 0:

        top_body = pygame.transform.scale(
            pipe_body,
            (
                body_width,
                top_body_height
            )
        )

    else:

        top_body = None


    # Bottom body

    bottom_body_height = (
        playable_height
        - gap_bottom
        - cap_height
    )


    if bottom_body_height > 0:

        bottom_body = pygame.transform.scale(
            pipe_body,
            (
                body_width,
                bottom_body_height
            )
        )

    else:

        bottom_body = None


    pipes.append(
        {
            "x": x,
            "gap_top": gap_top,
            "gap_bottom": gap_bottom,
            "top_body": top_body,
            "bottom_body": bottom_body,
            "passed": False
        }
    )


# Draw pipe

def draw_pipe(pipe):

    x = int(pipe["x"])

    gap_top = int(
        pipe["gap_top"]
    )

    gap_bottom = int(
        pipe["gap_bottom"]
    )

    cap_width = pipe_cap.get_width()

    cap_height = pipe_cap.get_height()

    body_width = pipe_body.get_width()


    # Body follows pipe

    body_x = (
        x
        + (cap_width - body_width) // 2
    )


    # Top body

    if pipe["top_body"] is not None:

        screen.blit(
            pipe["top_body"],
            (
                body_x,
                0
            )
        )


    # Top cap

    screen.blit(
        top_pipe_cap,
        (
            x,
            gap_top - cap_height
        )
    )


    # Bottom body

    if pipe["bottom_body"] is not None:

        screen.blit(
            pipe["bottom_body"],
            (
                body_x,
                gap_bottom + cap_height
            )
        )


    # Bottom cap

    screen.blit(
        pipe_cap,
        (
            x,
            gap_bottom
        )
    )


# Pipe collision rectangles

def get_pipe_rects(pipe):

    x = int(pipe["x"])

    gap_top = int(
        pipe["gap_top"]
    )

    gap_bottom = int(
        pipe["gap_bottom"]
    )

    pipe_width = pipe_cap.get_width()

    screen_height = screen.get_height()

    floor_height = floor_image.get_height()


    top_rect = pygame.Rect(
        x,
        0,
        pipe_width,
        gap_top
    )


    bottom_rect = pygame.Rect(
        x,
        gap_bottom,
        pipe_width,
        (
            screen_height
            - floor_height
            - gap_bottom
        )
    )


    return (
        top_rect,
        bottom_rect
    )


# Draw floor

def draw_floor():

    floor_width = floor_image.get_width()

    floor_height = floor_image.get_height()

    y = (
        screen.get_height()
        - floor_height
    )

    x = 0


    while x < screen.get_width():

        screen.blit(
            floor_image,
            (
                x,
                y
            )
        )

        x += floor_width


# Clock

clock = pygame.time.Clock()


# Main loop

running = True

while running:

    # Handle events

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        # Window resize

        if event.type == pygame.VIDEORESIZE:

            screen = pygame.display.set_mode(
                (
                    event.w,
                    event.h
                ),
                pygame.RESIZABLE
            )

            pipes.clear()

            last_gap_center = None


        # Keyboard controls

        if event.type == pygame.KEYDOWN:

            if game_over:

                if event.key == pygame.K_SPACE:

                    reset_game()

            else:

                if event.key == pygame.K_SPACE:

                    bird_velocity = (
                        flap_strength
                    )

                    flap_sound.play()


        # Mouse / touch controls

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:

                reset_game()

            else:

                bird_velocity = (
                    flap_strength
                )

                flap_sound.play()


    # Current screen size

    screen_width = screen.get_width()

    screen_height = screen.get_height()

    floor_height = floor_image.get_height()


    # Gameplay

    if not game_over:

        # Bird animation

        animation_timer += (
            clock.get_time()
        )


        if animation_timer >= animation_speed:

            animation_timer -= (
                animation_speed
            )

            bird_frame += 1


            if bird_frame >= len(
                bird_frames
            ):

                bird_frame = 0


        # Bird physics

        bird_velocity += gravity

        bird_y += bird_velocity


        # Bird image

        bird_image = bird_frames[
            bird_frame
        ]

        bird_rect = bird_image.get_rect(
            center=(
                int(bird_x),
                int(bird_y)
            )
        )


        # Spawn pipes

        if len(pipes) == 0:

            create_pipe()

        else:

            last_pipe = pipes[-1]


            if (
                last_pipe["x"]
                <= screen_width
                - PIPE_DISTANCE
            ):

                create_pipe()


        # Move pipes

        for pipe in pipes:

            pipe["x"] -= PIPE_SPEED


            # Pipe passed

            if (
                not pipe["passed"]
                and pipe["x"]
                + pipe_cap.get_width()
                < bird_x
            ):

                pipe["passed"] = True

                score += 1

                point_sound.play()


                # Update high score

                if score > high_score:

                    high_score = score


                # Increase speed every 5 pipes

                if score % 5 == 0:

                    PIPE_SPEED += (
                        PIPE_SPEED_INCREASE
                    )


        # Remove old pipes

        pipe_width = pipe_cap.get_width()

        pipes = [
            pipe
            for pipe in pipes
            if (
                pipe["x"]
                + pipe_width
                > 0
            )
        ]


        # Pipe collision

        for pipe in pipes:

            top_rect, bottom_rect = (
                get_pipe_rects(pipe)
            )


            if bird_rect.colliderect(
                top_rect
            ):

                die()


            if bird_rect.colliderect(
                bottom_rect
            ):

                die()


        # Ceiling collision

        if bird_rect.top <= 0:

            bird_y = (
                bird_rect.height
                // 2
            )

            bird_velocity = 0


        # Floor collision

        if bird_rect.bottom >= (
            screen_height
            - floor_height
        ):

            die()


    else:

        # Keep bird visible

        bird_image = bird_frames[
            bird_frame
        ]

        bird_rect = bird_image.get_rect(
            center=(
                int(bird_x),
                int(bird_y)
            )
        )


    # Draw background

    screen.fill(SKY)


    # Draw pipes

    for pipe in pipes:

        draw_pipe(pipe)


    # Draw floor

    draw_floor()


    # Draw bird

    screen.blit(
        bird_image,
        bird_rect
    )


    # Draw current score

    if not game_over:

        draw_number(
            score,
            screen_width // 2,
            40
        )


    # Draw high score label

    highscore_text = font.render(
        "Highscore ",
        True,
        (255, 255, 255)
    )

    screen.blit(
        highscore_text,
        (
            20,
            20
        )
    )


    # Draw high score number

    draw_number_left(
        high_score,
        160,
        20
    )


    # Draw game over

    if game_over:

        gameover_rect = (
            gameover_image.get_rect(
                center=(
                    screen_width // 2,
                    screen_height // 2
                )
            )
        )

        screen.blit(
            gameover_image,
            gameover_rect
        )


    # Update display

    pygame.display.flip()


    # Limit FPS

    clock.tick(60)


pygame.quit()