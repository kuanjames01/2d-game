
import pygame
import random
import math


class Explosion:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.timer = 0
        self.duration = 0.55

        self.particles = []

        # Pixel-art explosion colors
        self.colors = [
            (255, 255, 120),  # Bright yellow
            (255, 220, 40),   # Yellow
            (255, 150, 20),   # Orange
            (255, 70, 100),   # Pink
            (220, 30, 140),   # Magenta
            (130, 50, 190)    # Purple
        ]

        # Create explosion particles
        for _ in range(65):

            angle = random.uniform(0, math.pi * 2)
            speed = random.randint(35, 160)

            size = random.choice([3, 4, 5, 6])

            color = random.choice(self.colors)

            self.particles.append({
                "x": float(x),
                "y": float(y),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "size": size,
                "color": color
            })

        # Create small surrounding sparkles
        self.sparkles = []

        for _ in range(15):

            angle = random.uniform(0, math.pi * 2)
            distance = random.randint(20, 45)

            self.sparkles.append({
                "x": x + math.cos(angle) * distance,
                "y": y + math.sin(angle) * distance,
                "size": random.randint(2, 5),
                "color": random.choice([
                    (130, 70, 220),
                    (50, 100, 255),
                    (255, 30, 180),
                    (255, 220, 40)
                ])
            })

    def update(self, dt):

        self.timer += dt

        for particle in self.particles:

            particle["x"] += particle["vx"] * dt
            particle["y"] += particle["vy"] * dt

            # Slow down particles
            particle["vx"] *= 0.96
            particle["vy"] *= 0.96

    def draw(self, screen):

        progress = self.timer / self.duration

        # Draw explosion particles
        if progress < 1:

            for particle in self.particles:

                x = int(particle["x"])
                y = int(particle["y"])

                size = particle["size"]

                pygame.draw.rect(
                    screen,
                    particle["color"],
                    (x, y, size, size)
                )

        # Bright central flash
        if self.timer < 0.12:

            flash_size = 10

            pygame.draw.rect(
                screen,
                (255, 255, 120),
                (
                    int(self.x - flash_size // 2),
                    int(self.y - flash_size // 2),
                    flash_size,
                    flash_size
                )
            )

            # Cross-shaped sparkle
            pygame.draw.rect(
                screen,
                (255, 255, 230),
                (int(self.x - 2), int(self.y - 12), 4, 24)
            )

            pygame.draw.rect(
                screen,
                (255, 255, 230),
                (int(self.x - 12), int(self.y - 2), 24, 4)
            )

        # Draw surrounding pixel sparkles
        if progress < 0.7:

            for sparkle in self.sparkles:

                pygame.draw.rect(
                    screen,
                    sparkle["color"],
                    (
                        int(sparkle["x"]),
                        int(sparkle["y"]),
                        sparkle["size"],
                        sparkle["size"]
                    )
                )

    def is_finished(self):

        return self.timer >= self.duration
