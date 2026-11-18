
import pygame

from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


def draw_hud(screen, font, health, score, endless_survival_time=None):
    health_text = font.render(f"Health: {health}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)

    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))

    if endless_survival_time is not None:
        total_seconds = int(endless_survival_time)
        minutes, seconds = divmod(total_seconds, 60)
        survival_text = font.render(
            f"Endless Survival: {minutes:02d}:{seconds:02d}",
            True,
            WHITE
        )
        screen.blit(survival_text, (10, 70))


def draw_game_over(screen, big_font, font, score):

    # Dark transparent overlay
    overlay = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    overlay.set_alpha(180)
    overlay.fill(BLACK)

    screen.blit(overlay, (0, 0))

    # Game Over title
    title = big_font.render("GAME OVER", True, (255, 50, 50))
    title_rect = title.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
    )
    screen.blit(title, title_rect)

    # Final score
    score_text = font.render(
        f"Final Score: {score}",
        True,
        WHITE
    )
    score_rect = score_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )
    screen.blit(score_text, score_rect)

    # Instructions
    restart_text = font.render(
        "Press R to Restart",
        True,
        WHITE
    )
    restart_rect = restart_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    )
    screen.blit(restart_text, restart_rect)

    quit_text = font.render(
        "Press ESC to Quit",
        True,
        WHITE
    )
    quit_rect = quit_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
    )
    screen.blit(quit_text, quit_rect)
