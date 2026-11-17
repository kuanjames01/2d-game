
import pygame
import os

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED
)


class Player:

    def __init__(self):

        self.width = 70
        self.height = 70

        # Get project directory
        BASE_PATH = os.path.dirname(os.path.dirname(__file__))

        # Spaceship image path
        IMAGE_PATH = os.path.join(
            BASE_PATH,
            "assets",
            "images",
            "spaceship.png"
        )

        # Load spaceship
        self.image = pygame.image.load(IMAGE_PATH)

        # Preserve transparency and optimize after display initialization
        if pygame.display.get_surface() is not None:
            self.image = self.image.convert_alpha()

        self.image = pygame.transform.smoothscale(
            self.image,
            (self.width, self.height)
        )

        # Set spaceship position
        self.rect = self.image.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 100
            )
        )

        self.speed = PLAYER_SPEED

    def update(self, keys, dt):

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed * dt

        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed * dt

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed * dt

        # Keep player inside screen
        self.rect.clamp_ip(
            pygame.Rect(
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

    def draw(self, screen):

        # Draw spaceship
        screen.blit(self.image, self.rect)
