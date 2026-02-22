from Circleshape import CircleShape
from constants import SHOT_RADIUS
import pygame

class Shot(CircleShape):
    
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
    
    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.position, self.radius, SHOT_RADIUS)
    
    def update(self, dt):
        self.position += self.velocity * dt