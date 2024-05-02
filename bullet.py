from movable import *


class BulletType:
    TYPE = {
        # value field: lives, img_name, cost (number of coins), is_purchased by the user
        "L1": [1, "bulletL0", 0.5,True],
        "L2": [2, "bulletL2", 0.75,False],
        "L3": [3, "bullet3", 1,False]
    }

    def __init__(self, bullet_type: str):
        self.lives, self.img_name, self.cost,_ = BulletType.TYPE[bullet_type]


class Bullet(Movable):
    SPEED = 4

    def __init__(self, init_pos, velocity, surface, b_type: BulletType = BulletType("L1")):
        super().__init__(init_pos, velocity, load_sprite(b_type.img_name), surface=surface, lives=b_type.lives)

    def move(self):
        self.pos += self.velocity
