from movable import *
from bullet import Bullet
from asteroid import Asteroid
from util import vec_size, timer, load_sprite
from shield import Shield


class SpaceShip(Movable):
    MANVRBTY = 5
    ACC = 0.1
    # the initial angle is vertically upwards
    UP = Vector2(0, -1)

    def __init__(self, init_pos: tuple, create_bullet_callback, surface):
        super().__init__(init_pos, (0, 0), load_sprite('spaceship'), surface=surface,
                         lives=Asteroid.BIG_ASTEROID_LIVES * 4)
        self.dir = Vector2(self.UP)
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")

        # miscellaneous
        self.shield = None
        self.__params=None

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params):
        self.__params = params
        self.shield = Shield((0, 0), self.surface, params["shield_type"])

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        ang = self.MANVRBTY * sign
        self.dir.rotate_ip(ang)

    # skills that the spaceship has:
    def shoot(self) -> bool:
        if self.params["bullet_num"] <= 0:
            return False
        bullet_velocity = self.dir * Bullet.SPEED
        bullet = Bullet(self.pos, bullet_velocity, self.surface, b_type=self.params["bullet_type"])
        self.create_bullet_callback(bullet)
        self.laser_sound.play()
        self.params["bullet_num"] -= 1
        return True

    def start_shield(self):
        if self.params["shield_num"] <= 0:
            return False
        self.shield.enable_shield()
        # set a time range for the shield to show
        timer(self.params["shield_type"].duration, self.shield.disable_shield)
        self.params["shield_num"] -= 1
        return True

    def acc(self):
        velocity = self.velocity + self.dir * self.ACC
        curr_speed = vec_size(self.velocity)
        if curr_speed - Bullet.SPEED < 0:
            self.velocity = velocity
        elif vec_size(velocity) - curr_speed < 0:
            self.velocity = velocity

    def draw(self):
        ang = self.dir.angle_to(self.UP)
        rotated_surface = rotozoom(self.img, ang, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_pos = self.pos - rotated_surface_size * 0.5
        self.surface.blit(rotated_surface, blit_pos)
        if self.shield.is_show():
            self.shield.pos=self.pos
            self.shield.draw()

    def add_shield(self) -> bool:
        if self.params["coin_num"] > self.params["shield_type"].cost:
            self.params["coin_num"] -= self.params["shield_type"].cost
            self.params["shield_num"] += 1
            return True
        return False

    def add_bullet(self) -> bool:
        if self.params["coin_num"] > self.params["bullet_type"].cost:
            self.params["coin_num"] -= self.params["bullet_type"].cost
            self.params["bullet_num"] += 1
            return True
        return False
