from movable import *
from util import load_sprite,resize_img
import random


class Coin(Movable):
    def __init__(self, surface, game_obj):
        super().__init__(Coin.coin_pos(game_obj), sprite=resize_img(load_sprite("coin"),0.03), velocity=Vector2(0, 0), lives=0,
                         surface=surface)

    @staticmethod
    def rand_in_range(num, range_):
        return random.uniform(num - range_ / 2, num + range_ / 2)

    # place the coin onto the game_object that is eliminated (there is a range)
    @staticmethod
    def coin_pos(game_obj):
        x = game_obj.pos.x
        y = game_obj.pos.y
        return Vector2(Coin.rand_in_range(x, 50), Coin.rand_in_range(y, 50))
