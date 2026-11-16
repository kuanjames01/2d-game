
import pygame
from game.settings import YELLOW, BULLET_SPEED


class Bullet:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y, 6, 15)
        self.speed = BULLET_SPEED

    def update(self, dt):
        self.rect.y -= self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            YELLOW,
            self.rect,
            border_radius=3
        )

    def is_off_screen(self):
        return self.rect.bottom < 0
