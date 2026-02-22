import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import asyncio
from screen import draw_game_over_screen, draw_title_screen


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
                draw_game_over_screen(screen, score)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        if event.type == pygame.KEYDOWN:
                            waiting = False
                    clock.tick(60)
                    await asyncio.sleep(0)
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
