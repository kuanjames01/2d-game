
import pygame
import random
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
    BULLET_FIRE_INTERVAL
)

from game.player import Player
from game.bullet import Bullet
from game.meteor import Meteor
from game.collision import check_bullet_meteor_collisions


# Initialize Pygame
pygame.init()

# Create window
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(GAME_TITLE)

# Game clock
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Create player
player = Player()

# Create bullets
bullets = []

# Create meteorites
meteors = []

# Player health and score
health = PLAYER_HEALTH
score = 0

# Meteor spawn timer
meteor_spawn_timer = 0
bullet_fire_timer = 0
elapsed_time = 0

# Generate background stars
stars = []

for _ in range(80):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    stars.append((x, y))


# Main game loop
running = True

while running:

    # Calculate delta time
    dt = clock.tick(FPS) / 1000

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

    # Get keyboard input
    keys = pygame.key.get_pressed()

    # Keep shooting automatically, starting immediately
    bullet_fire_timer += dt * 1000
    if bullet_fire_timer >= BULLET_FIRE_INTERVAL:
        bullets.append(Bullet(player.rect.centerx, player.rect.top))
        bullet_fire_timer = 0

    # Update player
    player.update(keys, dt)

    # Update bullets
    for bullet in bullets[:]:

        bullet.update(dt)

        if bullet.is_off_screen():
            bullets.remove(bullet)

    # Spawn meteorites
    meteor_spawn_timer += dt * 1000
    elapsed_time += dt

    if meteor_spawn_timer >= METEOR_SPAWN_INTERVAL:

        meteors.append(Meteor(elapsed_time))

        meteor_spawn_timer = 0

    # Update meteorites
    for meteor in meteors[:]:

        meteor.update(dt)

        if meteor.is_off_screen():
            meteors.remove(meteor)

    # Check bullet and meteor collisions
    destroyed_meteors = check_bullet_meteor_collisions(bullets, meteors)
    score += destroyed_meteors * METEOR_SCORE

    # Meteors damage the player on contact and are removed after the collision
    for meteor in meteors[:]:
        if player.rect.colliderect(meteor.rect):
            meteors.remove(meteor)
            health = max(0, health - 1)

    # Draw background
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        pygame.draw.circle(
            screen,
            WHITE,
            star,
            1
        )

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)

    # Draw meteorites
    for meteor in meteors:
        meteor.draw(screen)

    # Draw player
    player.draw(screen)

    # Draw health and score
    health_text = font.render(f"Health: {health}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))

    # Update display
    pygame.display.flip()


# Close game
pygame.quit()
sys.exit()
