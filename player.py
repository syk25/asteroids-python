from Circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
import pygame
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, touch_controls=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_timer = 0
        self.touch_controls = touch_controls
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_cooldown_timer -= dt

        rotate_input = 0.0
        thrust_input = 0.0
        shoot_input = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            rotate_input -= 1.0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            rotate_input += 1.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            thrust_input += 1.0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            thrust_input -= 1.0
        if keys[pygame.K_SPACE]:
            shoot_input = True

        if self.touch_controls:
            t_rotate, t_thrust, t_shoot = self.touch_controls.get_input()
            rotate_input += t_rotate
            thrust_input += t_thrust
            shoot_input = shoot_input or t_shoot

        if rotate_input:
            self.rotate(rotate_input * dt)
        if thrust_input:
            self.move(thrust_input * dt)
        if shoot_input:
            self.shoot()
            
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    def shoot(self):
        if self.shoot_cooldown_timer > 0:
            return
        self.shoot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position[0], self.position[1])
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

