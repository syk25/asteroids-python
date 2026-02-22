from Circleshape import CircleShape
import pygame
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import random
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
    
    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return False

        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        first_asteroid_vector = self.velocity.rotate(random_angle)
        second_asteroid_vector = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        first_asteroid = Asteroid(self.position[0],self.position[1], new_radius)
        second_asteroid = Asteroid(self.position[0],self.position[1], new_radius)
        first_asteroid.velocity = first_asteroid_vector * 1.2
        second_asteroid.velocity = second_asteroid_vector
        return True



        pass