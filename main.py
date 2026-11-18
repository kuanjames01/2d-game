
import pygame
import random
import math
import sys

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    BLACK,
    WHITE,
    METEOR_SPAWN_INTERVAL,
    PLAYER_HEALTH,
    METEOR_SCORE,
    BULLET_FIRE_INTERVAL,
    BOSS_START_TIME,
    BOSS_SCORE,
    BOSS_MAX_LEVEL
)

from game.player import Player
from game.bullet import Bullet
from game.meteor import Meteor
from game.boss import MeteorDestroyer
from game.explosion import Explosion
from game.collision import (
    check_boss_hazard_collisions,
    check_bullet_boss_collisions,
    check_bullet_meteor_collisions
)
from game.ui import draw_hud, draw_game_over
from game.audio import create_game_sounds


# ==========================================
# INITIALIZE PYGAME AND AUDIO
# ==========================================

pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=1,
    buffer=512
)

try:
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=1,
        buffer=512
    )
except pygame.error as exc:
    raise RuntimeError(
        "Pygame could not open an audio device. Run the game with Windows "
        "Python (not the WSL interpreter) and verify that Windows has an "
        "active output device."
    ) from exc

pygame.display.init()
pygame.font.init()


# ==========================================
# CREATE GAME WINDOW
# ==========================================

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 80)


# ==========================================
# CREATE GAME SOUNDS
# ==========================================

sounds = create_game_sounds()


# ==========================================
# BACKGROUND STARS
# ==========================================

stars = []

for _ in range(80):

    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)

    stars.append((x, y))


# ==========================================
# GAME VARIABLES
# ==========================================

player = None

bullets = []
meteors = []
explosions = []
boss_projectiles = []
boss = None
boss_level = 1
next_boss_time = BOSS_START_TIME
endless_mode = False
endless_survival_time = 0

health = PLAYER_HEALTH
score = 0

meteor_spawn_timer = 0
bullet_fire_timer = 0
elapsed_time = 0

game_over = False


# ==========================================
# RESET GAME
# ==========================================

def reset_game():

    global player
    global bullets
    global meteors
    global explosions
    global boss_projectiles
    global boss
    global boss_level
    global next_boss_time
    global endless_mode
    global endless_survival_time

    global health
    global score

    global meteor_spawn_timer
    global bullet_fire_timer
    global elapsed_time

    global game_over

    player = Player()

    bullets = []
    meteors = []
    explosions = []
    boss_projectiles = []
    boss = None
    boss_level = 1
    next_boss_time = BOSS_START_TIME
    endless_mode = False
    endless_survival_time = 0

    health = PLAYER_HEALTH
    score = 0

    meteor_spawn_timer = 0
    bullet_fire_timer = 0
    elapsed_time = 0

    game_over = False


def spawn_meteor_wave(elapsed_time):

    wave_size = min(3, 1 + int(elapsed_time // 60))
    speed_scale = 1 + 0.45 * math.log1p(elapsed_time / 120)

    if wave_size == 1:
        x_positions = [random.randint(30, SCREEN_WIDTH - 30)]
    elif wave_size == 2:
        center_x = random.randint(60, SCREEN_WIDTH - 60)
        spread = random.randint(35, 75)
        x_positions = [
            max(30, min(SCREEN_WIDTH - 30, center_x - spread)),
            max(30, min(SCREEN_WIDTH - 30, center_x + spread))
        ]
    else:
        center_x = random.randint(70, SCREEN_WIDTH - 70)
        spread = random.randint(45, 85)
        x_positions = [
            max(30, center_x - spread),
            center_x,
            min(SCREEN_WIDTH - 30, center_x + spread)
        ]

    staggered = wave_size > 1 and random.random() < 0.5

    for index, x in enumerate(x_positions):
        meteor = Meteor(
            elapsed_time,
            x=x,
            speed_scale=speed_scale
        )
        if staggered:
            meteor.rect.bottom = -index * 55
        meteors.append(meteor)


# Start game
reset_game()


# ==========================================
# MAIN GAME LOOP
# ==========================================

running = True

while running:

    dt = clock.tick(FPS) / 1000

    # --------------------------------------
    # HANDLE EVENTS
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            # Restart game
            if game_over and event.key == pygame.K_r:
                reset_game()


    # Get keyboard input
    keys = pygame.key.get_pressed()


    # ======================================
    # GAMEPLAY
    # ======================================

    if not game_over:

        # ----------------------------------
        # AUTOMATIC SHOOTING
        # ----------------------------------

        bullet_fire_timer += dt * 1000

        if bullet_fire_timer >= BULLET_FIRE_INTERVAL:

            bullets.append(
                Bullet(
                    player.rect.centerx,
                    player.rect.top
                )
            )

            sounds["shoot"].play()

            bullet_fire_timer = 0


        # ----------------------------------
        # UPDATE PLAYER
        # ----------------------------------

        player.update(keys, dt)


        # ----------------------------------
        # UPDATE BULLETS
        # ----------------------------------

        for bullet in bullets[:]:

            bullet.update(dt)

            if bullet.is_off_screen():
                bullets.remove(bullet)


        # ----------------------------------
        # START THE BOSS FIGHT
        # ----------------------------------
        elapsed_time += dt

        if (
            boss is None
            and not endless_mode
            and boss_level <= BOSS_MAX_LEVEL
            and elapsed_time >= next_boss_time
        ):
            boss = MeteorDestroyer(level=boss_level)

        # SPAWN NORMAL METEORS
        # ----------------------------------

        meteor_spawn_timer += dt * 1000

        spawn_interval = max(
            350,
            METEOR_SPAWN_INTERVAL / (1 + elapsed_time / 180)
        )

        if meteor_spawn_timer >= spawn_interval:

            spawn_meteor_wave(elapsed_time)

            meteor_spawn_timer -= spawn_interval

        # ----------------------------------
        # UPDATE METEORS
        # ----------------------------------

        for meteor in meteors[:]:

            meteor.update(dt)

            if meteor.is_off_screen():
                meteors.remove(meteor)


        # ----------------------------------
        # BULLET AND METEOR COLLISIONS
        # ----------------------------------

        destroyed_meteors = check_bullet_meteor_collisions(
            bullets,
            meteors
        )


        # ----------------------------------
        # UPDATE SCORE
        # ----------------------------------

        score += len(destroyed_meteors) * METEOR_SCORE


        # ----------------------------------
        # UPDATE BOSS
        # ----------------------------------

        if boss is not None:

            if check_bullet_boss_collisions(bullets, boss):

                defeated_level = boss.level
                score += BOSS_SCORE * defeated_level
                boss = None
                if defeated_level >= BOSS_MAX_LEVEL:
                    endless_mode = True
                    endless_survival_time = 0
                else:
                    boss_level = defeated_level + 1
                    next_boss_time = elapsed_time + BOSS_START_TIME

            else:

                boss.update(
                    dt,
                    player,
                    meteors,
                    elapsed_time,
                    boss_projectiles
                )

        # ----------------------------------
        # UPDATE BOSS ATTACKS
        # ----------------------------------

        for hazard in boss_projectiles[:]:
            hazard.update(dt, player)
            if hazard.is_finished():
                boss_projectiles.remove(hazard)

        hazard_damage = check_boss_hazard_collisions(
            player,
            boss_projectiles
        )

        if hazard_damage:
            health = max(0, health - hazard_damage)
            sounds["damage"].play()


        # ----------------------------------
        # CREATE EXPLOSIONS
        # ----------------------------------

        for position in destroyed_meteors:

            explosions.append(
                Explosion(
                    position[0],
                    position[1]
                )
            )

            sounds["explosion"].play()


        # ----------------------------------
        # METEOR AND PLAYER COLLISIONS
        # ----------------------------------

        for meteor in meteors[:]:

            if player.rect.colliderect(meteor.rect):

                meteors.remove(meteor)

                health = max(0, health - 1)

                sounds["damage"].play()


        # ----------------------------------
        # CHECK GAME OVER
        # ----------------------------------

        if health <= 0:

            game_over = True

        if endless_mode:
            endless_survival_time += dt


    # ======================================
    # UPDATE EXPLOSIONS
    # ======================================

    for explosion in explosions[:]:

        explosion.update(dt)

        if explosion.is_finished():
            explosions.remove(explosion)


    # ======================================
    # DRAW BACKGROUND
    # ======================================

    screen.fill(BLACK)

    for star in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            star,
            1
        )


    # ======================================
    # DRAW BULLETS
    # ======================================

    for bullet in bullets:
        bullet.draw(screen)


    # ======================================
    # DRAW METEORS
    # ======================================

    for meteor in meteors:
        meteor.draw(screen)

    for hazard in boss_projectiles:
        hazard.draw(screen)

    if boss is not None:
        boss.draw(screen, font)


    # ======================================
    # DRAW EXPLOSIONS
    # ======================================

    for explosion in explosions:
        explosion.draw(screen)


    # ======================================
    # DRAW PLAYER
    # ======================================

    player.draw(screen)


    # ======================================
    # DRAW HUD
    # ======================================

    draw_hud(
        screen,
        font,
        health,
        score,
        endless_survival_time if endless_mode else None
    )


    # ======================================
    # DRAW GAME OVER
    # ======================================

    if game_over:

        draw_game_over(
            screen,
            big_font,
            font,
            score
        )


    # Update display
    pygame.display.flip()


# ==========================================
# CLOSE GAME
# ==========================================

pygame.quit()
sys.exit()
