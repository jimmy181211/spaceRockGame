from pygame.math import Vector2
from util import get_rand_velocity, load_sprite, wrap_pos, load_sound
from pygame.transform import rotozoom


class Movable:
    def __init__(self, init_pos, velocity, sprite, surface, lives):
        self.curr_lives = lives
        self.lives=lives
        self.pos = Vector2(init_pos)
        self.velocity = Vector2(velocity)
        self.img = sprite
        self.radius = self.img.get_width() / 2
        self.surface = surface
        self.is_die = False

    def draw(self):
        blit_pos = self.pos - Vector2(self.radius)
        self.surface.blit(self.img, blit_pos)

    def move(self):
        self.pos = wrap_pos(self.pos + self.velocity, self.surface)

    def _collide(self, obj):
        dist = self.pos.distance_to(obj.pos)
        if dist - (self.radius + obj.radius) < 0:
            return True
        else:
            return False

    def collide(self, obj):
        if self._collide(obj):
            if self.curr_lives >= obj.curr_lives:
                self.curr_lives -= obj.curr_lives
                obj.is_die = True
            if self.curr_lives <= obj.curr_lives:
                obj.curr_lives -= self.curr_lives
                self.is_die = True
            return True
        return False
