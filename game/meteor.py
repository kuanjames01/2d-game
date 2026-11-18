
import pygame
import random
import os

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    METEOR_SPEED,
    METEOR_BASE_HEALTH,
    METEOR_HEALTH_INCREASE_INTERVAL
)


# Image directory
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
IMAGE_PATH = os.path.join(BASE_PATH, "assets", "images")


# Grey meteors: large and slow
GREY_METEORS = [
    "meteorGrey_big1.png",
    "meteorGrey_big2.png",
    "meteorGrey_big3.png",
    "meteorGrey_big4.png"
]

# Brown meteors: small and fast
BROWN_METEORS = [
    "meteorBrown_med1.png",
    "meteorBrown_med3.png"
]


# Load images without requiring display initialization
GREY_IMAGES = [
    pygame.image.load(
        os.path.join(IMAGE_PATH, filename)
    )
    for filename in GREY_METEORS
]

BROWN_IMAGES = [
    pygame.image.load(
        os.path.join(IMAGE_PATH, filename)
    )
    for filename in BROWN_METEORS
]


class Meteor:

    def __init__(
        self,
        elapsed_time=0,
        x=None,
        y=None,
        velocity=None,
        small=False,
        speed=None,
        speed_scale=1.0
    ):

        # Difficulty level
        difficulty_level = int(
            elapsed_time // METEOR_HEALTH_INCREASE_INTERVAL
        )

        # Randomly choose meteor type
        self.is_grey = False if small else random.choice([True, False])

        if self.is_grey:

            # Large and slow grey meteor
            original_image = random.choice(GREY_IMAGES)

            self.radius = random.randint(30, 42)

            self.speed = random.uniform(
                METEOR_SPEED * 0.6,
                METEOR_SPEED * 0.9
            )

            self.health = (
                METEOR_BASE_HEALTH + 2 + difficulty_level
            )

        else:

            # Small and fast brown meteor
            original_image = random.choice(BROWN_IMAGES)

            self.radius = random.randint(14, 23)

            self.speed = random.uniform(
                METEOR_SPEED * 1.3,
                METEOR_SPEED * 1.8
            )

            self.health = (
                max(1, METEOR_BASE_HEALTH - 1)
                + difficulty_level
            )

        self.speed *= speed_scale

        # Resize meteor image
        self.size = self.radius * 2

        if speed is not None:
            self.speed = speed

        self.image = pygame.transform.smoothscale(
            original_image,
            (self.size, self.size)
        )

        # Random horizontal position
        if x is None:
            x = random.randint(
                self.radius,
                SCREEN_WIDTH - self.radius
            )

        # Spawn above screen
        if y is None:
            y = -self.size

        self.rect = self.image.get_rect(
            center=(x, y)
        )
        self.velocity = (
            velocity if velocity is not None else (0, self.speed)
        )

    def update(self, dt):

        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt

    def draw(self, screen):

        # Draw meteor sprite
        screen.blit(self.image, self.rect)

    def is_off_screen(self):

        return self.rect.top > SCREEN_HEIGHT
