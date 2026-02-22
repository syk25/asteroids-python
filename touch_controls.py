import pygame

JOYSTICK_RADIUS = 60
THUMB_RADIUS = 25
DEADZONE = 10
MAX_THROW = 50


class TouchControls:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Left side: virtual joystick (rotate + thrust)
        self.joystick_finger_id = None
        self.joystick_origin = None
        self.joystick_current = None

        # Right side: shoot button
        self.shoot_finger_id = None
        self.is_shooting = False

    def reset(self):
        self.joystick_finger_id = None
        self.joystick_origin = None
        self.joystick_current = None
        self.shoot_finger_id = None
        self.is_shooting = False

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            x = event.x * self.screen_width
            y = event.y * self.screen_height
            if x < self.screen_width / 2:
                if self.joystick_finger_id is None:
                    self.joystick_finger_id = event.finger_id
                    self.joystick_origin = pygame.Vector2(x, y)
                    self.joystick_current = pygame.Vector2(x, y)
            else:
                if self.shoot_finger_id is None:
                    self.shoot_finger_id = event.finger_id
                    self.is_shooting = True

        elif event.type == pygame.FINGERUP:
            if event.finger_id == self.joystick_finger_id:
                self.joystick_finger_id = None
                self.joystick_origin = None
                self.joystick_current = None
            elif event.finger_id == self.shoot_finger_id:
                self.shoot_finger_id = None
                self.is_shooting = False

        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self.joystick_finger_id:
                x = event.x * self.screen_width
                y = event.y * self.screen_height
                self.joystick_current = pygame.Vector2(x, y)

    def get_input(self):
        """Returns (rotate_factor, thrust_factor, shoot).
        rotate_factor: -1..1 (negative=left, positive=right)
        thrust_factor: -1..1 (positive=forward, negative=backward)
        """
        rotate = 0.0
        thrust = 0.0

        if self.joystick_origin and self.joystick_current:
            delta = self.joystick_current - self.joystick_origin
            if abs(delta.x) > DEADZONE:
                rotate = max(-1.0, min(1.0, delta.x / MAX_THROW))
            if abs(delta.y) > DEADZONE:
                thrust = max(-1.0, min(1.0, -delta.y / MAX_THROW))

        return rotate, thrust, self.is_shooting

    def draw(self, screen):
        # Left virtual joystick
        jx = int(self.screen_width * 0.15)
        jy = int(self.screen_height * 0.82)

        if self.joystick_origin:
            origin = (int(self.joystick_origin.x), int(self.joystick_origin.y))
            pygame.draw.circle(screen, (100, 100, 100), origin, JOYSTICK_RADIUS, 2)

            delta = self.joystick_current - self.joystick_origin
            if delta.length() > MAX_THROW:
                delta = delta.normalize() * MAX_THROW
            thumb_pos = (
                int(self.joystick_origin.x + delta.x),
                int(self.joystick_origin.y + delta.y),
            )
            pygame.draw.circle(screen, (200, 200, 200), thumb_pos, THUMB_RADIUS, 2)
        else:
            pygame.draw.circle(screen, (50, 50, 50), (jx, jy), JOYSTICK_RADIUS, 2)

        # Right shoot button
        sx = int(self.screen_width * 0.85)
        sy = int(self.screen_height * 0.82)
        btn_color = (180, 60, 60) if self.is_shooting else (50, 50, 50)
        pygame.draw.circle(screen, btn_color, (sx, sy), 45, 2)

        font = pygame.font.SysFont(None, 28)
        text_color = (200, 80, 80) if self.is_shooting else (100, 100, 100)
        text = font.render("FIRE", True, text_color)
        screen.blit(text, text.get_rect(center=(sx, sy)))
