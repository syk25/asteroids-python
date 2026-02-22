import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import asyncio


def draw_title_screen(screen, show_title):
    font_title = pygame.font.SysFont(None, 80)
    font_keys = pygame.font.SysFont(None, 36)
    font_hint = pygame.font.SysFont(None, 28)

    screen.fill("black")

    if show_title:
        title = font_title.render("ASTEROIDS", True, "white")
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)))

    controls = [
        ("W / Up",    "Move forward"),
        ("S / Down",  "Move backward"),
        ("A / Left",  "Rotate left"),
        ("D / Right", "Rotate right"),
        ("Space",     "Shoot"),
    ]

    start_y = SCREEN_HEIGHT // 2 - (len(controls) * 40) // 2
    for i, (key, action) in enumerate(controls):
        y = start_y + i * 40
        key_surf = font_keys.render(key, True, (200, 200, 50))
        action_surf = font_keys.render(action, True, "white")
        screen.blit(key_surf, key_surf.get_rect(right=SCREEN_WIDTH // 2 - 20, centery=y))
        screen.blit(action_surf, action_surf.get_rect(left=SCREEN_WIDTH // 2 + 20, centery=y))

    hint = font_hint.render("Press any key to start", True, (150, 150, 150))
    screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)))

    pygame.display.flip()


async def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    player = None
    score = 0

    def reset_game():
        nonlocal player, score
        score = 0
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()

        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable)
        Shot.containers = (shots, drawable, updatable)

        AsteroidField()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Title screen
    waiting = True
    blink_timer = 0
    blink_interval = 0.5
    show_title = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                waiting = False
        blink_timer += clock.tick(60) / 1000
        if blink_timer >= blink_interval:
            blink_timer -= blink_interval
            show_title = not show_title
        draw_title_screen(screen, show_title)
        await asyncio.sleep(0)

    reset_game()

    while True:

        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        for thing in drawable:
            thing.draw(screen)

        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                reset_game()
                break

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += 100
                    if asteroid.split():
                        score += 50

        font_score = pygame.font.SysFont(None, 36)
        score_surf = font_score.render(f"Score: {score}", True, "white")
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
