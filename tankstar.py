import pygame
import random
from pathlib import Path
from pygame import mixer

pygame.init()
mixer.init()

# ============================================================
# SCREEN
# ============================================================

WIDTH = 794
HEIGHT = 528

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tankstar: Space Assault")

clock = pygame.time.Clock()
FPS = 60

BASE_FOLDER = Path(__file__).parent
ASSET_FOLDER = BASE_FOLDER / "assets"
SCORE_FILE = BASE_FOLDER / "scores.txt"


# ============================================================
# LOAD SPRITE
# ============================================================

def load_sprite(filename, max_width, max_height):

    image = pygame.image.load(
        ASSET_FOLDER / filename
    ).convert_alpha()

    bounds = image.get_bounding_rect()

    if bounds.width > 0 and bounds.height > 0:
        image = image.subsurface(bounds).copy()

    scale = min(
        max_width / image.get_width(),
        max_height / image.get_height()
    )

    new_width = int(image.get_width() * scale)
    new_height = int(image.get_height() * scale)

    return pygame.transform.smoothscale(
        image,
        (new_width, new_height)
    )


# ============================================================
# ASSETS
# ============================================================

background = pygame.image.load(
    ASSET_FOLDER / "background.png"
).convert()

background = pygame.transform.smoothscale(
    background,
    (WIDTH, HEIGHT)
)

player_img = load_sprite(
    "player_ship.png",
    70,
    80
)

enemy_img = load_sprite(
    "enemy_ship.png",
    75,
    70
)

boss_img = load_sprite(
    "boss_ship.png",
    220,
    145
)

player_bullet_img = load_sprite(
    "player_bullet.png",
    13,
    35
)

enemy_bullet_img = load_sprite(
    "enemy_bullet.png",
    13,
    35
)

# Enemy bullets travel downward
enemy_bullet_img = pygame.transform.rotate(
    enemy_bullet_img,
    180
)

explosion_img = load_sprite(
    "explosion.png",
    120,
    120
)

pygame.display.set_icon(player_img)


# ============================================================
# SOUND
# ============================================================

def load_sound(filename):

    try:
        return mixer.Sound(
            ASSET_FOLDER / filename
        )
    except:
        return None


shoot_sound = load_sound("shoot.wav")
explosion_sound = load_sound("explosion.wav")


# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
BLUE = (60, 150, 255)

RED = (255, 45, 45)
DARK_RED = (120, 0, 0)

YELLOW = (255, 220, 40)

BLACK = (5, 7, 20)
GRAY = (160, 170, 190)
GREEN = (50, 230, 120)


# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont(
    "arial",
    22,
    bold=True
)

small_font = pygame.font.SysFont(
    "arial",
    16,
    bold=True
)

title_font = pygame.font.SysFont(
    "arial",
    42,
    bold=True
)

menu_font = pygame.font.SysFont(
    "arial",
    25,
    bold=True
)

warning_font = pygame.font.SysFont(
    "arial",
    52,
    bold=True
)

game_over_font = pygame.font.SysFont(
    "arial",
    46,
    bold=True
)


# ============================================================
# SCOREBOARD
# ============================================================

def load_scores():

    if not SCORE_FILE.exists():
        return []

    try:

        with open(SCORE_FILE, "r") as file:

            scores = []

            for line in file:

                line = line.strip()

                if line.isdigit():
                    scores.append(int(line))

            scores.sort(reverse=True)

            return scores[:5]

    except:
        return []


def save_score(new_score):

    scores = load_scores()

    scores.append(new_score)

    scores.sort(reverse=True)

    scores = scores[:5]

    with open(SCORE_FILE, "w") as file:

        for value in scores:
            file.write(str(value) + "\n")


# ============================================================
# TEXT
# ============================================================

def draw_text(
        text,
        color,
        x,
        y,
        selected_font=font,
        center=False
):

    shadow = selected_font.render(
        text,
        True,
        BLACK
    )

    rendered = selected_font.render(
        text,
        True,
        color
    )

    if center:

        rect = rendered.get_rect(
            center=(x, y)
        )

        shadow_rect = shadow.get_rect(
            center=(x + 2, y + 2)
        )

        screen.blit(
            shadow,
            shadow_rect
        )

        screen.blit(
            rendered,
            rect
        )

    else:

        screen.blit(
            shadow,
            (x + 2, y + 2)
        )

        screen.blit(
            rendered,
            (x, y)
        )


# ============================================================
# BUTTON
# ============================================================

def draw_button(
        text,
        rect,
        mouse_position
):

    hovered = rect.collidepoint(
        mouse_position
    )

    if hovered:

        background_color = (
            25,
            90,
            150
        )

        border_color = CYAN

    else:

        background_color = (
            12,
            30,
            65
        )

        border_color = BLUE


    pygame.draw.rect(
        screen,
        background_color,
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        border_color,
        rect,
        2,
        border_radius=8
    )

    draw_text(
        text,
        WHITE,
        rect.centerx,
        rect.centery,
        menu_font,
        True
    )


# ============================================================
# BACKGROUND PARTICLES
# ============================================================

stars = []

for i in range(45):

    stars.append(
        [
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.randint(1, 3)
        ]
    )


def update_stars():

    for star in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            star[2]
        )

        star[1] += star[2]

        if star[1] > HEIGHT:

            star[0] = random.randint(
                0,
                WIDTH
            )

            star[1] = 0


# ============================================================
# EXPLOSIONS
# ============================================================

explosions = []


def create_explosion(x, y, size=100):

    explosions.append(
        {
            "x": x,
            "y": y,
            "timer": 18,
            "size": size
        }
    )


def update_explosions():

    for explosion in explosions[:]:

        timer = explosion["timer"]

        scale = (
            explosion["size"]
            -
            timer
        )

        scale = max(
            30,
            scale
        )

        image = pygame.transform.smoothscale(
            explosion_img,
            (scale, scale)
        )

        screen.blit(
            image,
            (
                explosion["x"]
                -
                scale // 2,

                explosion["y"]
                -
                scale // 2
            )
        )

        explosion["timer"] -= 1

        if explosion["timer"] <= 0:
            explosions.remove(explosion)


# ============================================================
# GAME VARIABLES
# ============================================================

PLAYER_SPEED = 5

PLAYER_BULLET_SPEED = 11

PLAYER_FIRE_DELAY = 230

SCORE_PER_ENEMY = 10

BOSS_SCORE = 100

MAX_LIVES = 3


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global player_x
    global player_y

    global player_bullets
    global enemy_bullets
    global boss_bullets

    global last_player_shot

    global enemy_x
    global enemy_y
    global enemy_speed
    global enemy_fire_timer

    global score
    global level
    global lives

    global boss_active
    global boss_warning

    global warning_start

    global boss_x
    global boss_y
    global boss_speed
    global boss_health
    global boss_max_health
    global boss_fire_timer

    global game_over
    global victory

    global invincible_until

    global score_saved


    # --------------------------------------------------------
    # PLAYER
    # --------------------------------------------------------

    player_x = (
        WIDTH // 2
        -
        player_img.get_width() // 2
    )

    player_y = (
        HEIGHT
        -
        player_img.get_height()
        -
        20
    )

    player_bullets = []

    last_player_shot = 0


    # --------------------------------------------------------
    # NORMAL ENEMY
    # --------------------------------------------------------

    enemy_x = random.randint(
        40,
        WIDTH
        -
        enemy_img.get_width()
        -
        40
    )

    enemy_y = 65

    enemy_speed = 2.3

    enemy_fire_timer = random.randint(
        60,
        120
    )

    enemy_bullets = []


    # --------------------------------------------------------
    # GAME
    # --------------------------------------------------------

    score = 0

    level = 1

    lives = MAX_LIVES

    invincible_until = 0


    # --------------------------------------------------------
    # BOSS
    # --------------------------------------------------------

    boss_active = False

    boss_warning = False

    warning_start = 0

    boss_x = 0
    boss_y = -200

    boss_speed = 2.2

    boss_max_health = 40

    boss_health = boss_max_health

    boss_fire_timer = 100

    boss_bullets = []


    game_over = False

    victory = False

    score_saved = False

    explosions.clear()


# ============================================================
# START BOSS
# ============================================================

def start_boss():

    global boss_active

    global boss_x
    global boss_y

    global boss_fire_timer

    global enemy_bullets


    boss_active = True

    boss_x = (
        WIDTH // 2
        -
        boss_img.get_width() // 2
    )

    boss_y = -boss_img.get_height()

    boss_fire_timer = 80

    enemy_bullets.clear()


# ============================================================
# PLAYER HIT
# ============================================================

def damage_player():

    global lives
    global game_over
    global invincible_until


    current_time = pygame.time.get_ticks()

    if current_time < invincible_until:
        return


    lives -= 1

    invincible_until = (
        current_time
        +
        1200
    )


    create_explosion(
        player_x
        +
        player_img.get_width() // 2,

        player_y
        +
        player_img.get_height() // 2,

        100
    )


    if explosion_sound:
        explosion_sound.play()


    if lives <= 0:
        game_over = True


# ============================================================
# MAIN MENU
# ============================================================

start_button = pygame.Rect(
    WIDTH // 2 - 110,
    245,
    220,
    52
)

score_button = pygame.Rect(
    WIDTH // 2 - 110,
    312,
    220,
    52
)

exit_button = pygame.Rect(
    WIDTH // 2 - 110,
    379,
    220,
    52
)


def draw_main_menu():

    mouse_position = pygame.mouse.get_pos()

    screen.blit(
        background,
        (0, 0)
    )

    update_stars()


    overlay = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    overlay.set_alpha(80)

    overlay.fill(
        (0, 0, 15)
    )

    screen.blit(
        overlay,
        (0, 0)
    )


    draw_text(
        "TANKSTAR",
        CYAN,
        WIDTH // 2,
        115,
        title_font,
        True
    )


    draw_text(
        "SPACE ASSAULT",
        WHITE,
        WIDTH // 2,
        165,
        font,
        True
    )


    draw_button(
        "START",
        start_button,
        mouse_position
    )

    draw_button(
        "SCOREBOARD",
        score_button,
        mouse_position
    )

    draw_button(
        "EXIT",
        exit_button,
        mouse_position
    )


    draw_text(
        "Survive the enemy fleet and destroy the final boss.",
        GRAY,
        WIDTH // 2,
        470,
        small_font,
        True
    )


# ============================================================
# SCOREBOARD SCREEN
# ============================================================

def draw_scoreboard():

    screen.blit(
        background,
        (0, 0)
    )

    update_stars()


    overlay = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    overlay.set_alpha(135)

    overlay.fill(
        (0, 0, 20)
    )

    screen.blit(
        overlay,
        (0, 0)
    )


    draw_text(
        "TOP SCORES",
        YELLOW,
        WIDTH // 2,
        90,
        title_font,
        True
    )


    scores = load_scores()


    if not scores:

        draw_text(
            "No scores yet",
            WHITE,
            WIDTH // 2,
            190,
            font,
            True
        )

    else:

        for index, value in enumerate(scores):

            draw_text(
                f"{index + 1}.   {value}",
                WHITE,
                WIDTH // 2,
                170 + index * 45,
                font,
                True
            )


    draw_text(
        "Press ESC to return",
        CYAN,
        WIDTH // 2,
        450,
        small_font,
        True
    )


# ============================================================
# INITIAL STATE
# ============================================================

reset_game()

state = "menu"

run = True


# ============================================================
# MAIN LOOP
# ============================================================

while run:

    clock.tick(FPS)

    current_time = pygame.time.get_ticks()


    # ========================================================
    # MENU
    # ========================================================

    if state == "menu":

        draw_main_menu()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if start_button.collidepoint(
                            event.pos
                    ):

                        reset_game()

                        state = "game"


                    elif score_button.collidepoint(
                            event.pos
                    ):

                        state = "scoreboard"


                    elif exit_button.collidepoint(
                            event.pos
                    ):

                        run = False


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    reset_game()

                    state = "game"


        pygame.display.update()

        continue


    # ========================================================
    # SCOREBOARD
    # ========================================================

    if state == "scoreboard":

        draw_scoreboard()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    state = "menu"


        pygame.display.update()

        continue


    # ========================================================
    # GAME EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                state = "menu"


            if event.key == pygame.K_r:

                if game_over or victory:

                    reset_game()

                    state = "game"


    # ========================================================
    # BACKGROUND
    # ========================================================

    screen.blit(
        background,
        (0, 0)
    )

    update_stars()


    # ========================================================
    # BOSS WARNING
    # ========================================================

    if boss_warning:

        # Flash red overlay
        if (
            current_time // 250
        ) % 2 == 0:

            warning_overlay = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            warning_overlay.set_alpha(75)

            warning_overlay.fill(
                DARK_RED
            )

            screen.blit(
                warning_overlay,
                (0, 0)
            )


        draw_text(
            "WARNING!",
            RED,
            WIDTH // 2,
            HEIGHT // 2 - 35,
            warning_font,
            True
        )


        draw_text(
            "BOSS INCOMING",
            RED,
            WIDTH // 2,
            HEIGHT // 2 + 30,
            title_font,
            True
        )


        if (
            current_time
            -
            warning_start
            >
            2600
        ):

            boss_warning = False

            start_boss()


        pygame.display.update()

        continue


    # ========================================================
    # GAMEPLAY
    # ========================================================

    if not game_over and not victory:

        keys = pygame.key.get_pressed()


        # ----------------------------------------------------
        # PLAYER MOVEMENT
        # ----------------------------------------------------

        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED


        if keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED


        player_x = max(
            0,
            min(
                player_x,
                WIDTH
                -
                player_img.get_width()
            )
        )


        # ----------------------------------------------------
        # PLAYER SHOOTING
        # ----------------------------------------------------

        if (
            keys[pygame.K_SPACE]
            or
            keys[pygame.K_s]
        ):

            if (
                current_time
                -
                last_player_shot
                >=
                PLAYER_FIRE_DELAY
            ):

                bullet_x = (
                    player_x
                    +
                    player_img.get_width() // 2
                    -
                    player_bullet_img.get_width() // 2
                )

                bullet_y = (
                    player_y
                    -
                    player_bullet_img.get_height()
                )

                player_bullets.append(
                    [
                        bullet_x,
                        bullet_y
                    ]
                )

                last_player_shot = current_time

                if shoot_sound:
                    shoot_sound.play()


        # ----------------------------------------------------
        # PLAYER BULLETS
        # ----------------------------------------------------

        for bullet in player_bullets[:]:

            bullet[1] -= PLAYER_BULLET_SPEED


            screen.blit(
                player_bullet_img,
                (
                    bullet[0],
                    bullet[1]
                )
            )


            if bullet[1] < -40:

                player_bullets.remove(
                    bullet
                )


        # ====================================================
        # NORMAL ENEMY
        # ====================================================

        if not boss_active:

            enemy_x += enemy_speed


            if (
                enemy_x
                >=
                WIDTH
                -
                enemy_img.get_width()
            ):

                enemy_speed = -abs(
                    enemy_speed
                )


            if enemy_x <= 0:

                enemy_speed = abs(
                    enemy_speed
                )


            # ------------------------------------------------
            # ENEMY FIRING
            # ------------------------------------------------

            enemy_fire_timer -= 1


            if enemy_fire_timer <= 0:

                enemy_bullets.append(
                    [
                        enemy_x
                        +
                        enemy_img.get_width() // 2,

                        enemy_y
                        +
                        enemy_img.get_height(),

                        0,

                        5
                        +
                        level * 0.3
                    ]
                )


                enemy_fire_timer = random.randint(
                    max(
                        30,
                        90 - level * 5
                    ),

                    max(
                        50,
                        130 - level * 5
                    )
                )


            enemy_rect = pygame.Rect(
                enemy_x,
                enemy_y,
                enemy_img.get_width(),
                enemy_img.get_height()
            )


            # ------------------------------------------------
            # PLAYER BULLET VS ENEMY
            # ------------------------------------------------

            for bullet in player_bullets[:]:

                bullet_rect = pygame.Rect(
                    bullet[0],
                    bullet[1],
                    player_bullet_img.get_width(),
                    player_bullet_img.get_height()
                )


                if bullet_rect.colliderect(
                        enemy_rect
                ):

                    player_bullets.remove(
                        bullet
                    )


                    create_explosion(
                        enemy_rect.centerx,
                        enemy_rect.centery,
                        90
                    )


                    if explosion_sound:
                        explosion_sound.play()


                    score += SCORE_PER_ENEMY


                    level = (
                        score // 20
                        +
                        1
                    )


                    enemy_x = random.randint(
                        20,
                        WIDTH
                        -
                        enemy_img.get_width()
                        -
                        20
                    )


                    direction = 1

                    if enemy_speed < 0:
                        direction = -1


                    enemy_speed = (
                        2.3
                        +
                        level * 0.25
                    ) * direction


                    # ----------------------------------------
                    # BOSS TRIGGER
                    # ----------------------------------------

                    if (
                        score >= BOSS_SCORE
                        and
                        not boss_active
                    ):

                        boss_warning = True

                        warning_start = (
                            pygame.time.get_ticks()
                        )

                        enemy_bullets.clear()

                        player_bullets.clear()


                    break


        # ====================================================
        # BOSS
        # ====================================================

        if boss_active:

            # Boss enters screen
            if boss_y < 55:

                boss_y += 2


            else:

                boss_x += boss_speed


                if (
                    boss_x <= 10
                    or
                    boss_x
                    +
                    boss_img.get_width()
                    >=
                    WIDTH - 10
                ):

                    boss_speed *= -1


            # ------------------------------------------------
            # BOSS PHASE
            # ------------------------------------------------

            health_ratio = (
                boss_health
                /
                boss_max_health
            )


            if health_ratio > 0.66:

                boss_phase = 1

                bullet_count = 2

                boss_bullet_speed = 4.5

                fire_delay = 65


            elif health_ratio > 0.33:

                boss_phase = 2

                bullet_count = 3

                boss_bullet_speed = 5.5

                fire_delay = 48


            else:

                boss_phase = 3

                bullet_count = 5

                boss_bullet_speed = 6.5

                fire_delay = 34


            # ------------------------------------------------
            # BOSS FIRING
            # ------------------------------------------------

            boss_fire_timer -= 1


            if (
                boss_fire_timer <= 0
                and
                boss_y >= 50
            ):

                center_x = (
                    boss_x
                    +
                    boss_img.get_width() // 2
                )

                bullet_y = (
                    boss_y
                    +
                    boss_img.get_height()
                    -
                    15
                )


                # Spreading bullet pattern
                if bullet_count == 2:

                    velocities = [
                        (-1.0, boss_bullet_speed),
                        (1.0, boss_bullet_speed)
                    ]


                elif bullet_count == 3:

                    velocities = [
                        (-1.7, boss_bullet_speed),
                        (0, boss_bullet_speed),
                        (1.7, boss_bullet_speed)
                    ]


                else:

                    velocities = [
                        (-3.0, boss_bullet_speed),
                        (-1.5, boss_bullet_speed),
                        (0, boss_bullet_speed),
                        (1.5, boss_bullet_speed),
                        (3.0, boss_bullet_speed)
                    ]


                for vx, vy in velocities:

                    boss_bullets.append(
                        [
                            center_x,
                            bullet_y,
                            vx,
                            vy
                        ]
                    )


                boss_fire_timer = fire_delay


            # ------------------------------------------------
            # PLAYER BULLET VS BOSS
            # ------------------------------------------------

            boss_rect = pygame.Rect(
                boss_x,
                boss_y,
                boss_img.get_width(),
                boss_img.get_height()
            )


            for bullet in player_bullets[:]:

                bullet_rect = pygame.Rect(
                    bullet[0],
                    bullet[1],
                    player_bullet_img.get_width(),
                    player_bullet_img.get_height()
                )


                if bullet_rect.colliderect(
                        boss_rect
                ):

                    player_bullets.remove(
                        bullet
                    )

                    boss_health -= 1

                    score += 5


                    create_explosion(
                        bullet[0],
                        bullet[1],
                        45
                    )


                    if boss_health <= 0:

                        create_explosion(
                            boss_rect.centerx,
                            boss_rect.centery,
                            180
                        )


                        if explosion_sound:
                            explosion_sound.play()


                        score += 500

                        boss_active = False

                        boss_bullets.clear()

                        victory = True


                    break


        # ====================================================
        # NORMAL ENEMY BULLETS
        # ====================================================

        for bullet in enemy_bullets[:]:

            bullet[0] += bullet[2]

            bullet[1] += bullet[3]


            screen.blit(
                enemy_bullet_img,
                (
                    bullet[0],
                    bullet[1]
                )
            )


            if bullet[1] > HEIGHT:

                enemy_bullets.remove(
                    bullet
                )


        # ====================================================
        # BOSS BULLETS
        # ====================================================

        for bullet in boss_bullets[:]:

            bullet[0] += bullet[2]

            bullet[1] += bullet[3]


            screen.blit(
                enemy_bullet_img,
                (
                    bullet[0],
                    bullet[1]
                )
            )


            if (
                bullet[1] > HEIGHT
                or
                bullet[0] < -20
                or
                bullet[0] > WIDTH + 20
            ):

                boss_bullets.remove(
                    bullet
                )


        # ====================================================
        # PLAYER COLLISION
        # ====================================================

        player_rect = pygame.Rect(
            player_x,
            player_y,
            player_img.get_width(),
            player_img.get_height()
        )


        if current_time >= invincible_until:

            for bullet in enemy_bullets[:]:

                bullet_rect = pygame.Rect(
                    bullet[0],
                    bullet[1],
                    enemy_bullet_img.get_width(),
                    enemy_bullet_img.get_height()
                )


                if bullet_rect.colliderect(
                        player_rect
                ):

                    enemy_bullets.remove(
                        bullet
                    )

                    damage_player()

                    break


            for bullet in boss_bullets[:]:

                bullet_rect = pygame.Rect(
                    bullet[0],
                    bullet[1],
                    enemy_bullet_img.get_width(),
                    enemy_bullet_img.get_height()
                )


                if bullet_rect.colliderect(
                        player_rect
                ):

                    boss_bullets.remove(
                        bullet
                    )

                    damage_player()

                    break


    # ========================================================
    # DRAW ENEMY
    # ========================================================

    if (
        not boss_active
        and
        not boss_warning
        and
        not game_over
        and
        not victory
    ):

        screen.blit(
            enemy_img,
            (
                enemy_x,
                enemy_y
            )
        )


    # ========================================================
    # DRAW BOSS
    # ========================================================

    if boss_active:

        screen.blit(
            boss_img,
            (
                boss_x,
                boss_y
            )
        )


        # ----------------------------------------------------
        # BOSS HEALTH BAR
        # ----------------------------------------------------

        health_ratio = max(
            0,
            boss_health
            /
            boss_max_health
        )


        pygame.draw.rect(
            screen,
            DARK_RED,
            (
                195,
                62,
                400,
                16
            ),
            border_radius=5
        )


        pygame.draw.rect(
            screen,
            RED,
            (
                195,
                62,
                int(
                    400
                    *
                    health_ratio
                ),
                16
            ),
            border_radius=5
        )


        draw_text(
            "BOSS",
            WHITE,
            WIDTH // 2,
            50,
            small_font,
            True
        )


    # ========================================================
    # DRAW PLAYER
    # ========================================================

    if not game_over:

        # Blink when temporarily invincible
        should_draw = True


        if current_time < invincible_until:

            if (
                current_time // 100
            ) % 2 == 0:

                should_draw = False


        if should_draw:

            screen.blit(
                player_img,
                (
                    player_x,
                    player_y
                )
            )


    # ========================================================
    # EXPLOSIONS
    # ========================================================

    update_explosions()


    # ========================================================
    # HUD
    # ========================================================

    draw_text(
        f"SCORE: {score}",
        YELLOW,
        18,
        15
    )


    draw_text(
        f"LIVES: {lives}",
        RED,
        18,
        45
    )


    if not boss_active:

        draw_text(
            f"LEVEL: {level}",
            WHITE,
            WIDTH - 125,
            15
        )


    draw_text(
        "TANKSTAR",
        CYAN,
        WIDTH // 2,
        25,
        font,
        True
    )


    # ========================================================
    # GAME OVER
    # ========================================================

    if game_over:

        if not score_saved:

            save_score(score)

            score_saved = True


        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(185)

        overlay.fill(
            BLACK
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        draw_text(
            "GAME OVER",
            RED,
            WIDTH // 2,
            HEIGHT // 2 - 60,
            game_over_font,
            True
        )


        draw_text(
            f"Final Score: {score}",
            WHITE,
            WIDTH // 2,
            HEIGHT // 2 + 5,
            font,
            True
        )


        draw_text(
            "Press R to Restart",
            CYAN,
            WIDTH // 2,
            HEIGHT // 2 + 50,
            font,
            True
        )


        draw_text(
            "ESC - Main Menu",
            GRAY,
            WIDTH // 2,
            HEIGHT // 2 + 85,
            small_font,
            True
        )


    # ========================================================
    # VICTORY
    # ========================================================

    if victory:

        if not score_saved:

            save_score(score)

            score_saved = True


        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(180)

        overlay.fill(
            BLACK
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        draw_text(
            "MISSION COMPLETE",
            GREEN,
            WIDTH // 2,
            HEIGHT // 2 - 65,
            game_over_font,
            True
        )


        draw_text(
            "Boss Destroyed!",
            WHITE,
            WIDTH // 2,
            HEIGHT // 2,
            font,
            True
        )


        draw_text(
            f"Final Score: {score}",
            YELLOW,
            WIDTH // 2,
            HEIGHT // 2 + 38,
            font,
            True
        )


        draw_text(
            "Press R to Play Again",
            CYAN,
            WIDTH // 2,
            HEIGHT // 2 + 82,
            small_font,
            True
        )


    pygame.display.update()


pygame.quit()