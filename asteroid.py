from movable import *


class Asteroid(Movable):
    # size parameter determines the size of the asteroid
    # 3 denotes the biggest asteroid
    size_to_scale = {
        3: 1,
        2: 0.5,
        1: 0.25
    }
    BIG_ASTEROID_LIVES=4

    def __init__(self, init_pos, create_asteroid_callback, surface, size=3, lives=BIG_ASTEROID_LIVES):
        self.size = size
        self.create_asteroid_callback = create_asteroid_callback
        scale = self.size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        super().__init__(init_pos, get_rand_velocity(1, 3), sprite,surface=surface,lives=lives)

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.pos, self.create_asteroid_callback, surface=self.surface, size=self.size - 1, lives=int(self.lives / 2))
                self.create_asteroid_callback(asteroid)
        else:
            print("the asteroid is eliminated")

