import math
import random

import pygame

from game.meteor import Meteor
from game.settings import (
    BOSS_BARRAGE_METEOR_COUNT,
    BOSS_BARRAGE_SPEED,
    BOSS_HEALTH,
    BOSS_RAIN_METEOR_COUNT,
    METEOR_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)


ABILITY_COOLDOWNS = {
    "Meteor Rain": 8.0,
    "Meteor Barrage": 9.0,
    "Triple Laser": 7.0,
    "Homing Missiles": 9.0,
    "Energy Beam": 10.0,
    "Target Lock": 8.0,
    "Meteor Shield": 12.0,
    "Shockwave": 10.0,
    "Bullet Storm": 8.0,
    "Meteor Cluster": 9.0
}

ABILITY_NAMES = tuple(ABILITY_COOLDOWNS)

ABILITY_ATTACK_RECOVERY = {
    "Meteor Rain": 3.2,
    "Meteor Barrage": 2.6,
    "Triple Laser": 2.6,
    "Homing Missiles": 3.0,
    "Energy Beam": 2.5,
    "Target Lock": 2.5,
    "Meteor Shield": 3.8,
    "Shockwave": 4.2,
    "Bullet Storm": 2.6,
    "Meteor Cluster": 3.2
}


class BossHazard:

    def __init__(
        self,
        kind,
        x,
        y,
        damage,
        color=(255, 90, 90),
        velocity=(0, 0),
        size=14,
        lifetime=7.0,
        speed=0,
        charge_duration=0,
        active_duration=0,
        radius=48
    ):
        self.kind = kind
        self.x = float(x)
        self.y = float(y)
        self.damage = damage
        self.color = color
        self.velocity = velocity
        self.size = size
        self.lifetime = lifetime
        self.speed = speed
        self.charge_duration = charge_duration
        self.active_duration = active_duration
        self.radius = radius
        self.age = 0
        self.hit = False
        self.damage_timer = 0
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (round(self.x), round(self.y))
        self.max_radius = math.hypot(SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self, dt, player):
        self.age += dt
        self.damage_timer = max(0, self.damage_timer - dt)

        if self.kind == "homing":
            delta_x = player.rect.centerx - self.x
            delta_y = player.rect.centery - self.y
            distance = math.hypot(delta_x, delta_y)
            if distance:
                self.velocity = (
                    delta_x / distance * self.speed,
                    delta_y / distance * self.speed
                )

        if self.kind in ("projectile", "homing"):
            self.x += self.velocity[0] * dt
            self.y += self.velocity[1] * dt
            self.rect.center = (round(self.x), round(self.y))

            if (
                self.rect.right < 0
                or self.rect.left > SCREEN_WIDTH
                or self.rect.bottom < 0
                or self.rect.top > SCREEN_HEIGHT
            ):
                self.age = self.lifetime
        elif self.kind == "shockwave":
            self.radius += self.speed * dt

    def is_finished(self):
        if self.kind == "shockwave":
            return self.radius > self.max_radius
        return self.age >= self.lifetime

    def collides_with(self, player):
        if self.hit or self.age < self.charge_duration:
            return False

        if self.kind in ("projectile", "homing"):
            if self.rect.colliderect(player.rect):
                self.hit = True
                return True
            return False

        if self.kind == "beam":
            active = self.age < self.charge_duration + self.active_duration
            if not active or self.damage_timer > 0:
                return False
            beam_rect = pygame.Rect(
                round(self.x - 16),
                round(self.y),
                32,
                SCREEN_HEIGHT - round(self.y)
            )
            if beam_rect.colliderect(player.rect):
                self.damage_timer = 0.75
                return True
            return False

        if self.kind == "target":
            active = self.age < self.charge_duration + self.active_duration
            if not active:
                return False
            distance = math.hypot(
                player.rect.centerx - self.x,
                player.rect.centery - self.y
            )
            if distance <= self.radius + max(player.rect.width, player.rect.height) / 2:
                self.hit = True
                return True
            return False

        if self.kind == "shockwave":
            distance = math.hypot(
                player.rect.centerx - self.x,
                player.rect.centery - self.y
            )
            player_radius = max(player.rect.width, player.rect.height) / 2
            if abs(distance - self.radius) <= player_radius + 8:
                self.hit = True
                return True

        return False

    def draw(self, screen):
        if self.kind in ("projectile", "homing"):
            pygame.draw.circle(
                screen,
                self.color,
                self.rect.center,
                self.size // 2
            )
            pygame.draw.circle(
                screen,
                (255, 240, 180),
                self.rect.center,
                max(2, self.size // 5)
            )
        elif self.kind == "beam":
            beam_rect = pygame.Rect(
                round(self.x - 16),
                round(self.y),
                32,
                SCREEN_HEIGHT - round(self.y)
            )
            if self.age < self.charge_duration:
                pygame.draw.line(
                    screen,
                    (255, 170, 90),
                    (round(self.x), round(self.y)),
                    (round(self.x), SCREEN_HEIGHT),
                    3
                )
            elif self.age < self.charge_duration + self.active_duration:
                pygame.draw.rect(screen, self.color, beam_rect)
                pygame.draw.rect(screen, (255, 240, 180), beam_rect, 3)
        elif self.kind == "target":
            if self.age < self.charge_duration:
                pygame.draw.circle(
                    screen,
                    self.color,
                    (round(self.x), round(self.y)),
                    self.radius,
                    3
                )
            elif self.age < self.charge_duration + self.active_duration:
                pygame.draw.circle(
                    screen,
                    self.color,
                    (round(self.x), round(self.y)),
                    self.radius
                )
        elif self.kind == "shockwave":
            pygame.draw.circle(
                screen,
                self.color,
                (round(self.x), round(self.y)),
                max(1, round(self.radius)),
                5
            )


class MeteorDestroyer:

    def __init__(self, level=1):
        self.level = level
        self.width = 180
        self.height = 75
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - self.width) // 2,
            45,
            self.width,
            self.height
        )
        self.max_health = BOSS_HEALTH * (1 + 0.55 * (level - 1))
        self.health = self.max_health
        self.speed = 100 * (1 + 0.025 * (level - 1))
        self.direction = 1
        self.attack_damage = max(1, round(1 + 0.07 * (level - 1)))
        self.cooldown_scale = max(0.55, 1 - 0.025 * (level - 1))
        self.abilities = random.sample(ABILITY_NAMES, 3)
        self.ability_cooldowns = {
            ability: random.uniform(1.5, 3.0)
            for ability in self.abilities
        }
        self.attack_gap = 0
        self.shield_timer = 0
        self.ability_handlers = {
            "Meteor Rain": self._meteor_rain,
            "Meteor Barrage": self._meteor_barrage,
            "Triple Laser": self._triple_laser,
            "Homing Missiles": self._homing_missiles,
            "Energy Beam": self._energy_beam,
            "Target Lock": self._target_lock,
            "Meteor Shield": self._meteor_shield,
            "Shockwave": self._shockwave,
            "Bullet Storm": self._bullet_storm,
            "Meteor Cluster": self._meteor_cluster
        }

    def take_damage(self, damage):
        actual_damage = damage * (0.25 if self.shield_timer > 0 else 1)
        self.health = max(0, self.health - actual_damage)

    def update(self, dt, player, meteors, elapsed_time, hazards):
        self.rect.x += self.speed * self.direction * dt

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1

        self.shield_timer = max(0, self.shield_timer - dt)
        self.attack_gap = max(0, self.attack_gap - dt)
        for ability in self.ability_cooldowns:
            self.ability_cooldowns[ability] = max(
                0,
                self.ability_cooldowns[ability] - dt
            )

        if self.health <= 0 or self.attack_gap > 0:
            return

        ready_abilities = [
            ability
            for ability, cooldown in self.ability_cooldowns.items()
            if cooldown <= 0
        ]
        if not ready_abilities:
            return

        ability = random.choice(ready_abilities)
        self.ability_handlers[ability](
            player,
            meteors,
            elapsed_time,
            hazards
        )
        base_cooldown = ABILITY_COOLDOWNS[ability]
        self.ability_cooldowns[ability] = (
            base_cooldown * self.cooldown_scale
        )
        self.attack_gap = (
            ABILITY_ATTACK_RECOVERY[ability] * self.cooldown_scale
        )

    def _meteor_rain(self, player, meteors, elapsed_time, hazards):
        count = BOSS_RAIN_METEOR_COUNT
        positions = random.sample(range(24, SCREEN_WIDTH - 24), count)
        speed = METEOR_SPEED * (1 + 0.035 * (self.level - 1))
        for x in positions:
            meteors.append(
                Meteor(
                    elapsed_time,
                    x=x,
                    small=True,
                    speed=speed
                )
            )

    def _meteor_barrage(self, player, meteors, elapsed_time, hazards):
        target_x, target_y = player.rect.center
        speed = BOSS_BARRAGE_SPEED * (1 + 0.035 * (self.level - 1))
        for index in range(BOSS_BARRAGE_METEOR_COUNT):
            start_x = self.rect.left + (
                self.rect.width * (index + 1)
                // (BOSS_BARRAGE_METEOR_COUNT + 1)
            )
            start_y = self.rect.bottom
            delta_x = target_x - start_x
            delta_y = target_y - start_y
            distance = math.hypot(delta_x, delta_y)
            velocity = (
                (0, speed)
                if distance == 0
                else (delta_x / distance * speed, delta_y / distance * speed)
            )
            meteors.append(
                Meteor(
                    elapsed_time,
                    x=start_x,
                    y=start_y,
                    velocity=velocity,
                    small=True,
                    speed=speed
                )
            )

    def _triple_laser(self, player, meteors, elapsed_time, hazards):
        self._aimed_spread(player, hazards, (-0.25, 0, 0.25), 370)

    def _homing_missiles(self, player, meteors, elapsed_time, hazards):
        speed = 260 * (1 + 0.025 * (self.level - 1))
        for offset in (-45, 0, 45):
            hazards.append(
                BossHazard(
                    "homing",
                    self.rect.centerx + offset,
                    self.rect.bottom,
                    self.attack_damage,
                    color=(255, 125, 45),
                    size=18,
                    speed=speed,
                    lifetime=6
                )
            )

    def _energy_beam(self, player, meteors, elapsed_time, hazards):
        hazards.append(
            BossHazard(
                "beam",
                player.rect.centerx,
                self.rect.bottom,
                self.attack_damage,
                color=(255, 55, 55),
                charge_duration=0.9,
                active_duration=1.0,
                lifetime=1.9
            )
        )

    def _target_lock(self, player, meteors, elapsed_time, hazards):
        hazards.append(
            BossHazard(
                "target",
                player.rect.centerx,
                player.rect.centery,
                self.attack_damage,
                color=(255, 75, 75),
                charge_duration=1.1,
                active_duration=0.45,
                lifetime=1.55,
                radius=54
            )
        )

    def _meteor_shield(self, player, meteors, elapsed_time, hazards):
        self.shield_timer = 3.5

    def _shockwave(self, player, meteors, elapsed_time, hazards):
        hazards.append(
            BossHazard(
                "shockwave",
                self.rect.centerx,
                self.rect.centery,
                self.attack_damage,
                color=(100, 220, 255),
                speed=245 * (1 + 0.025 * (self.level - 1)),
                lifetime=5
            )
        )

    def _bullet_storm(self, player, meteors, elapsed_time, hazards):
        self._aimed_spread(
            player,
            hazards,
            (-0.75, -0.56, -0.37, -0.18, 0, 0.18, 0.37, 0.56, 0.75),
            310
        )

    def _meteor_cluster(self, player, meteors, elapsed_time, hazards):
        count = 7
        speed = METEOR_SPEED * 1.25 * (1 + 0.035 * (self.level - 1))
        for index in range(count):
            angle = math.pi / 2 + (index - (count - 1) / 2) * 0.16
            start_x = self.rect.centerx + (index - 3) * 17
            velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            meteors.append(
                Meteor(
                    elapsed_time,
                    x=start_x,
                    y=self.rect.bottom,
                    velocity=velocity,
                    small=True,
                    speed=speed
                )
            )

    def _aimed_spread(self, player, hazards, offsets, speed):
        delta_x = player.rect.centerx - self.rect.centerx
        delta_y = player.rect.centery - self.rect.bottom
        base_angle = math.atan2(delta_y, delta_x)
        scaled_speed = speed * (1 + 0.025 * (self.level - 1))
        for offset in offsets:
            angle = base_angle + offset
            hazards.append(
                BossHazard(
                    "projectile",
                    self.rect.centerx,
                    self.rect.bottom,
                    self.attack_damage,
                    velocity=(
                        math.cos(angle) * scaled_speed,
                        math.sin(angle) * scaled_speed
                    ),
                    size=13,
                    lifetime=6
                )
            )

    def draw(self, screen, font):
        body_color = (70, 190, 225) if self.shield_timer > 0 else (135, 75, 65)
        pygame.draw.rect(screen, body_color, self.rect, border_radius=10)
        pygame.draw.rect(
            screen,
            (205, 115, 70),
            self.rect,
            3,
            border_radius=10
        )

        label = font.render(
            f"METEOR DESTROYER - LEVEL {self.level}",
            True,
            (255, 255, 255)
        )
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
        remaining_width = int(
            bar_width * max(0, self.health) / self.max_health
        )
        health_rect = pygame.Rect(
            bar_rect.left,
            bar_rect.top,
            remaining_width,
            bar_height
        )
        pygame.draw.rect(screen, (50, 210, 80), health_rect)
        pygame.draw.rect(screen, (255, 255, 255), bar_rect, 2)

        if self.shield_timer > 0:
            pygame.draw.rect(
                screen,
                (100, 220, 255),
                self.rect.inflate(10, 10),
                3,
                border_radius=12
            )
