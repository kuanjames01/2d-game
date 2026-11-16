
import pygame
import math
import random
from array import array


SAMPLE_RATE = 44100


def generate_shoot_sound():

    samples = array("h")

    duration = 0.10

    for i in range(int(SAMPLE_RATE * duration)):

        t = i / SAMPLE_RATE
        progress = t / duration

        frequency = 1100 - (800 * progress)
        envelope = (1 - progress) ** 2

        value = math.sin(2 * math.pi * frequency * t)
        value *= envelope * 0.30

        samples.append(int(value * 32767))

    return pygame.mixer.Sound(buffer=samples.tobytes())


def generate_explosion_sound():

    samples = array("h")

    duration = 0.35

    for i in range(int(SAMPLE_RATE * duration)):

        t = i / SAMPLE_RATE
        progress = t / duration

        envelope = (1 - progress) ** 2

        # Low rumbling sound
        frequency = 100 - (65 * progress)

        boom = math.sin(2 * math.pi * frequency * t)

        # Random noise
        noise = random.uniform(-1, 1)

        value = (boom * 0.65 + noise * 0.35)
        value *= envelope * 0.65

        samples.append(
            max(-32768, min(32767, int(value * 32767)))
        )

    return pygame.mixer.Sound(buffer=samples.tobytes())


def generate_damage_sound():

    samples = array("h")

    duration = 0.20

    for i in range(int(SAMPLE_RATE * duration)):

        t = i / SAMPLE_RATE
        progress = t / duration

        frequency = 180 - (100 * progress)

        envelope = (1 - progress) ** 2

        value = math.sin(2 * math.pi * frequency * t)
        value *= envelope * 0.45

        samples.append(int(value * 32767))

    return pygame.mixer.Sound(buffer=samples.tobytes())


def create_game_sounds():

    if not pygame.mixer.get_init():
        raise pygame.error(
            "Initialize the Pygame mixer before creating game sounds."
        )

    sounds = {
        "shoot": generate_shoot_sound(),
        "explosion": generate_explosion_sound(),
        "damage": generate_damage_sound()
    }

    # Set individual sound volumes
    sounds["shoot"].set_volume(0.25)
    sounds["explosion"].set_volume(0.50)
    sounds["damage"].set_volume(0.40)

    return sounds
