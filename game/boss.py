import math
import random

import pygame

from game.meteor import Meteor
from game.settings import (
    BOSS_ATTACK_GAP,
    BOSS_BARRAGE_METEOR_COUNT,
    BOSS_BARRAGE_SPEED,
    BOSS_HEALTH,
    BOSS_METEOR_BARRAGE_COOLDOWN,
    BOSS_METEOR_RAIN_COOLDOWN,
    BOSS_RAIN_METEOR_COUNT,
    SCREEN_WIDTH
)


class MeteorDestroyer:

    def __init__(self):

        self.width = 180
        self.height = 75
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - self.width) // 2,
            45,
            self.width,
            self.height
        )

        self.health = BOSS_HEALTH
        self.speed = 100
        self.direction = 1

        self.rain_cooldown = BOSS_METEOR_RAIN_COOLDOWN
        self.barrage_cooldown = BOSS_METEOR_BARRAGE_COOLDOWN
        self.attack_gap = 0
        self.next_attack = "rain"

    def update(self, dt, player, meteors, elapsed_time):

        self.rect.x += self.speed * self.direction * dt

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1

        self.rain_cooldown -= dt
        self.barrage_cooldown -= dt
        self.attack_gap = max(0, self.attack_gap - dt)

        if self.attack_gap > 0:
            return

        if self.next_attack == "rain" and self.rain_cooldown <= 0:
            self._launch_meteor_rain(meteors, elapsed_time)
            self.rain_cooldown = BOSS_METEOR_RAIN_COOLDOWN
            self.next_attack = "barrage"
        elif self.next_attack == "barrage" and self.barrage_cooldown <= 0:
            self._launch_meteor_barrage(meteors, player, elapsed_time)
            self.barrage_cooldown = BOSS_METEOR_BARRAGE_COOLDOWN
            self.next_attack = "rain"
        elif self.rain_cooldown <= 0:
            self._launch_meteor_rain(meteors, elapsed_time)
            self.rain_cooldown = BOSS_METEOR_RAIN_COOLDOWN
            self.next_attack = "barrage"
        elif self.barrage_cooldown <= 0:
            self._launch_meteor_barrage(meteors, player, elapsed_time)
            self.barrage_cooldown = BOSS_METEOR_BARRAGE_COOLDOWN
            self.next_attack = "rain"
        else:
            return

        self.attack_gap = BOSS_ATTACK_GAP

    def _launch_meteor_rain(self, meteors, elapsed_time):

        x_positions = random.sample(
            range(23, SCREEN_WIDTH - 22),
            BOSS_RAIN_METEOR_COUNT
        )

        for x in x_positions:
            radius = random.randint(14, 23)
            meteors.append(
                Meteor(
                    elapsed_time,
                    x=x,
                    y=-radius * 2,
                    small=True
                )
            )

    def _launch_meteor_barrage(self, meteors, player, elapsed_time):

        target_x, target_y = player.rect.center

        for index in range(BOSS_BARRAGE_METEOR_COUNT):
            start_x = self.rect.left + (
                self.rect.width * (index + 1)
                // (BOSS_BARRAGE_METEOR_COUNT + 1)
            )
            start_y = self.rect.bottom
            delta_x = target_x - start_x
            delta_y = target_y - start_y
            distance = math.hypot(delta_x, delta_y)
            if distance == 0:
                velocity = (0, BOSS_BARRAGE_SPEED)
            else:
                velocity = (
                    delta_x / distance * BOSS_BARRAGE_SPEED,
                    delta_y / distance * BOSS_BARRAGE_SPEED
                )

            meteors.append(
                Meteor(
                    elapsed_time,
                    x=start_x,
                    y=start_y,
                    velocity=velocity,
                    small=True,
                    speed=BOSS_BARRAGE_SPEED
                )
            )

    def draw(self, screen, font):

        pygame.draw.rect(screen, (135, 75, 65), self.rect, border_radius=10)
        pygame.draw.rect(screen, (205, 115, 70), self.rect, 3, border_radius=10)

        label = font.render("METEOR DESTROYER", True, (255, 255, 255))
        label_rect = label.get_rect(
            center=(SCREEN_WIDTH // 2, self.rect.bottom + 16)
        )
        screen.blit(label, label_rect)

        bar_width = 400
        bar_height = 14
        bar_rect = pygame.Rect(
            (SCREEN_WIDTH - bar_width) // 2,
            10,
            bar_width,
            bar_height
        )
        pygame.draw.rect(screen, (80, 25, 25), bar_rect)

        remaining_width = int(bar_width * max(0, self.health) / BOSS_HEALTH)
        health_rect = pygame.Rect(
            bar_rect.left,
            bar_rect.top,
            remaining_width,
            bar_height
        )
        pygame.draw.rect(screen, (50, 210, 80), health_rect)
        pygame.draw.rect(screen, (255, 255, 255), bar_rect, 2)
