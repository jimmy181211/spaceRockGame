from util import load_sprite, resize_img
from movable import Movable


class ShieldType:
    TYPE = {
        # duration,image name, cost (number of coins), is purchased by the user
        "L1": [2, "shield", 3,True]
    }

    def __init__(self, type_str: str):
        self.duration, self.img_name, self.cost,_ = ShieldType.TYPE[type_str]


class Shield(Movable):
    def __init__(self, init_pos, surface, s_type: ShieldType = ShieldType("L1")):  # init_pos of type Vector2
        super().__init__(init_pos, (0, 0), resize_img(load_sprite(s_type.img_name),0.2), surface, 100)
        self.__is_show = False

    def is_show(self) -> bool:
        return self.__is_show

    def disable_shield(self):
        self.__is_show = False

    def enable_shield(self):
        self.__is_show=True

    def draw(self):
        super().draw()

    def shield_collide(self, game_obj):
        if self.__is_show and super()._collide(game_obj):
            # the obstacle moves away from the shield
            game_obj.pos-=(game_obj.velocity+self.velocity)
            game_obj.velocity = -1 * game_obj.velocity
