from ..utils.settings import *
from random import choice

# helper functions
# def make_shape(center, width, height):
#     """Create a pads/ball"""
#     surf = pygame.Surface((width, height), pygame.SRCALPHA)
#     rect = pygame.FRect(0, 0, width, height)
#     pygame.draw.rect(surf, FG_COLOR, rect)
#     return surf, surf.get_frect(center=center)


class Pad(pygame.sprite.Sprite):
    def __init__(self, pos, player, ball, groups):
        super().__init__(groups)
        self.start_x, self.start_y = pos
        self.player    = player
        self.ball      = ball
        self.direction = 0
        # self.image, self.rect = make_shape(pos, PAD_WIDTH, PAD_HEIGHT)

    def reset_position(self):
        self.rect.center = (self.start_x, self.start_y)

    def _move(self, dt):
        self.rect.y += self.direction * PAD_SPEED * dt
        self.rect.y = max(0, min(WINDOW_HEIGHT - PAD_HEIGHT, self.rect.y))

    def update(self, dt):
        if not self.ball.game_active:
            return
        self.set_direction()
        self._move(dt)


class PlayerPad(Pad):
    def __init__(seld, pos, player, ball, groups):
        super().__init__(pos, player, ball, groups)

    def set_direction(self):
        keys = pygame.key.get_pressed()
        if self.player == "player1":
            self.direction = -int(keys[pygame.K_w])  + int(keys[pygame.K_s])
        else:
            self.direction = -int(keys[pygame.K_UP]) + int(keys[pygame.K_DOWN])


class DumbOpponentPad(Pad):
    """Moves up and down cyclically, ignores the ball"""
    def __init__(self, pos, player, ball, groups):
        super().__init__(pos, player, ball, groups)

    def set_direction(self):
        if not self.ball.game_active:
            self.direction = 0
            return
        
        if self.rect.centery < self.ball.rect.centery:
            self.direction = 1
        elif self.rect.centery > self.ball.rect.centery:
            self.direction = -1
        else:
            self.direction = 0


class FollowOpponentPad(Pad):
    """Follows the ball"""
    def __init__(self, pos, player, ball, groups):
        super().__init__(pos, player, ball, groups)

    def set_direction(self):
        if not self.ball.game_active:
            self.direction = 0
            return

        if self.rect.centery < self.ball.rect.centery - PAD_HEIGHT // 2:
            self.direction = 1
        elif self.rect.centery > self.ball.rect.centery + PAD_HEIGHT // 2:
            self.direction = -1
        else:
            self.direction = 0


class SmartOpponentPad(Pad):
    """Predicts collision y coordinate & moves towards it. I haven't beaten it yet"""
    def __init__(self, pos, player, ball, groups):
        super().__init__(pos, player, ball, groups)

    def _predict_intercept_y(self) -> int:
        # x, y and t the ball will travel before pad hit
        dx_left = self.rect.centerx - self.ball.rect.centerx 
        t_left = abs(dx_left) / (abs(self.ball.direction.x) * BALL_SPEED)
        abs_y_left = self.ball.rect.centery + self.ball.direction.y * BALL_SPEED * t_left

        # adjust abs_y_left for bouncing off top/bottom, return remainder
        n = int(abs_y_left // WINDOW_HEIGHT)
        if n % 2 == 0:
            return int(abs_y_left % WINDOW_HEIGHT)
        else:
            return int(WINDOW_HEIGHT - (abs_y_left % WINDOW_HEIGHT))

    def set_direction(self):
        if not self.ball.game_active:
            self.direction = 0
            return

        target_y = self._predict_intercept_y()
        centre_y = self.rect.centery
        if centre_y < target_y:
            self.direction = 1
        elif centre_y > target_y:
            self.direction = -1
        else:
            self.direction = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, pads, scores, groups):
        super().__init__(groups)
        # self.image, self.rect = make_shape(pos, BALL_SIZE, BALL_SIZE)
        self.direction  = pygame.math.Vector2(choice([-1, 1]), choice([-1, 1]))
        self.pad_left, self.pad_right = pads
        self.game_active_ever = False
        self.game_active      = False
        self.scores     = scores
        self.collisions = 0

    def _reset_position(self):
        self.rect.midleft = POS['ball_start']
        self.direction = pygame.math.Vector2(choice([-1, 1]), choice([-1, 1]))
        self.pad_left.reset_position()
        self.pad_right.reset_position()
        self.game_active = False
        self.collisions = 0

    def _pad_hit(self, pad_rect, ball_rect):
        self.collisions += 1
        return pad_rect.top <= ball_rect.centery <= pad_rect.bottom
            
    def _return_to_bounds(self):
        if self.rect.top >= WINDOW_HEIGHT:
            self.rect.top = WINDOW_HEIGHT - 1
            self.direction.y = -1
        if self.rect.bottom <= 0:
            self.rect.bottom = 1
            self.direction.y = 1
            
    def _set_direction(self):
        self._return_to_bounds()

        # top & bottom
        if self.rect.top <= 0:
            self.rect.top = 0 
            self.direction.y =  abs(self.direction.y)
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y = -abs(self.direction.y)

        # left & right
        if self.rect.left <= PAD_WIDTH:
            if self._pad_hit(self.pad_left.rect, self.rect):
                self.direction.x = abs(self.direction.x)
            else:
                self.scores["player2"] += 1
                self._reset_position()

        elif self.rect.right > WINDOW_WIDTH - PAD_WIDTH:
            if self._pad_hit(self.pad_right.rect, self.rect):
                self.direction.x = -abs(self.direction.x)
            else:
                self.scores["player1"] += 1
                self._reset_position()

    def _move(self, dt):
        self.rect.center += self.direction * BALL_SPEED * dt * (1 + self.collisions / 10)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_active = True
            self.game_active_ever = True

        if self.game_active:
            self._set_direction()
            self._move(dt)
