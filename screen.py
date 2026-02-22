import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def draw_game_over_screen(screen, score):
    font_title = pygame.font.SysFont(None, 80)
    font_score = pygame.font.SysFont(None, 48)
    font_hint  = pygame.font.SysFont(None, 28)

    screen.fill("black")

    title = font_title.render("GAME OVER", True, "white")
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

    score_surf = font_score.render(f"Score: {score}", True, (200, 200, 50))
    screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    hint = font_hint.render("Tap or press any key to play again", True, (150, 150, 150))
    screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)))

    pygame.display.flip()


def draw_title_screen(screen, show_title):
    font_title = pygame.font.SysFont(None, 80)
    font_keys = pygame.font.SysFont(None, 36)
    font_hint = pygame.font.SysFont(None, 28)

    screen.fill("black")

    if show_title:
        title = font_title.render("ASTEROIDS", True, "white")
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)))

    controls = [
        ("W / Up",      "Move forward"),
        ("S / Down",    "Move backward"),
        ("A / Left",    "Rotate left"),
        ("D / Right",   "Rotate right"),
        ("Space",       "Shoot"),
        ("Left drag",   "Move / Rotate"),
        ("Right tap",   "Shoot"),
    ]

    start_y = SCREEN_HEIGHT // 2 - (len(controls) * 40) // 2
    for i, (key, action) in enumerate(controls):
        y = start_y + i * 40
        key_surf = font_keys.render(key, True, (200, 200, 50))
        action_surf = font_keys.render(action, True, "white")
        screen.blit(key_surf, key_surf.get_rect(right=SCREEN_WIDTH // 2 - 20, centery=y))
        screen.blit(action_surf, action_surf.get_rect(left=SCREEN_WIDTH // 2 + 20, centery=y))

    hint = font_hint.render("Tap or press any key to start", True, (150, 150, 150))
    screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)))

    pygame.display.flip()