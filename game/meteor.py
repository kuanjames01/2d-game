
import pygame
import random

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    METEOR_SPEED,
    METEOR_BASE_HEALTH,
    METEOR_HEALTH_INCREASE_INTERVAL
)


class Meteor:

    def __init__(self, elapsed_time=0):

        # Random meteorite size
        self.radius = random.randint(18, 35)
        difficulty_level = int(
            elapsed_time // METEOR_HEALTH_INCREASE_INTERVAL
        )
        self.health = METEOR_BASE_HEALTH + difficulty_level

        # Random horizontal position
        x = random.randint(
            self.radius,
            SCREEN_WIDTH - self.radius
        )

        # Spawn above the screen
        y = -self.radius * 2

        self.rect = pygame.Rect(
            x - self.radius,
            y,
            self.radius * 2,
            self.radius * 2
        )

        # Random falling speed
        self.speed = random.uniform(
            METEOR_SPEED * (0.7 + difficulty_level * 0.05),
            METEOR_SPEED * (1.4 + difficulty_level * 0.05)
        )

        # Meteorite color
        self.color = (120, 120, 130)

    def update(self, dt):

        # Move downward
        self.rect.y += self.speed * dt

    def draw(self, screen):

        # Draw meteorite
        pygame.draw.circle(
            screen,
            self.color,
            self.rect.center,
            self.radius
        )

        # Draw craters
        pygame.draw.circle(
            screen,
            (80, 80, 90),
            (self.rect.centerx - 8, self.rect.centery - 5),
            5
        )

        pygame.draw.circle(
            screen,
            (90, 90, 100),
            (self.rect.centerx + 9, self.rect.centery + 8),
            4
        )

    def is_off_screen(self):

        return self.rect.top > SCREEN_HEIGHT
