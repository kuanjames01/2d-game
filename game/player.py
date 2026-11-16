
import pygame
from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    BLUE
)


class Player:

    def __init__(self):
        self.width = 50
        self.height = 50

        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.width // 2,
            SCREEN_HEIGHT - 100,
            self.width,
            self.height
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

        # Keep player inside the screen
        self.rect.clamp_ip(
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def draw(self, screen):

        # Draw spaceship
        pygame.draw.polygon(
            screen,
            BLUE,
            [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.centerx, self.rect.bottom - 12),
                (self.rect.right, self.rect.bottom)
            ]
        )
