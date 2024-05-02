from abstrGame import AbstrGame
import pygame
from util import resize_img, load_sprite
from bullet import BulletType
from shield import ShieldType
from pygame.color import Color
from button import Button


class Shop(AbstrGame):
    def __init__(self, user_info: dict, user_fortune: dict):
        super().__init__("shop", "shop")
        self.user_info = user_info
        self.user_fortune = user_fortune
        self.margin = 10
        icons = {"coin_num": ("coin", 0.1), "shield_num": ("shield_icon", 0.1)}
        goods = {"bullet_type": ("bullet_icon", 0.2),
                 "shield_type": ("shield_icon", 0.3)}
        self.goods_details = {"bullet_type": BulletType.TYPE, "shield_type": ShieldType.TYPE}
        self.icons = {name: resize_img(load_sprite(icons[name][0]), icons[name][1]) for name in icons}
        self.goods = {name: resize_img(load_sprite(goods[name][0]), goods[name][1]) for name in goods}
        self.length = self.bg_w / (len(goods) + 1)
        self.goods_pos = {name: (self.length * (i + 1), self.bg_h / 2 - 100) for i, name in enumerate(self.goods)}

        self.icons_pos = {}  # position for the icons
        self.icons_txt_pos = {}  # position for the values displayed
        acc_icon = 0
        for cnt, label in enumerate(self.icons):
            img = self.icons[label]
            self.icons_pos[label] = (700, acc_icon + cnt * self.margin)
            self.icons_txt_pos[label] = (700 + self.margin + img.get_width(), acc_icon + cnt * self.margin)
            acc_icon += img.get_height()

        self.small_font = pygame.font.Font(None, 32)
        # determine the position of the texts
        self.txt_pos = {}
        for name in self.goods:
            pos = self.goods_pos[name]
            self.txt_pos[name] = (pos[0], pos[1] + self.goods[name].get_height() + self.margin)

        self.opt_bar = resize_img(load_sprite("shop_button"), 0.1)
        self.buttons = {}
        for name in self.goods:
            good_pos = self.goods_pos[name]
            sub_buttons = {}
            # retrieve weapon-level from the BulletType/ShieldType classes
            for cnt, label in enumerate(self.goods_details[name]):
                # find the center of the button
                center = (good_pos[0] + self.goods[name].get_width() + self.margin + self.opt_bar.get_width() / 2,
                          good_pos[1] + cnt * (self.opt_bar.get_height() + self.margin) + self.opt_bar.get_height() / 2)
                sub_buttons[label] = Button(center, label, img_name="shop_button",
                                            scale=0.1)
            self.buttons[name] = sub_buttons

    def _process_game_logic(self):
        pass

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._quit()

            # detect whether the mouse collides with the button
            label = ""
            good_type = ""
            for name in self.buttons:
                for l in self.buttons[name]:
                    lcl_label = self.buttons[name][l].collide(pygame.mouse.get_pos())
                    if lcl_label != "":
                        label=lcl_label
                        good_type = name
                        break

            print("label:",label,"good_type:",good_type)
            # is the button clicked
            if event.type == pygame.MOUSEBUTTONDOWN and label != "":
                print(self.goods_details)
                detail = self.goods_details[good_type][label]
                # detail[3] records whether the weapon is purchased
                if not detail[3]:
                    dif = self.user_fortune["coin_num"] - detail[2] * 3  # coin_num-cost of the bullet type
                    if dif >= 0:
                        self.user_fortune["coin_num"] = dif
                        # set the weapon to 'purchased state'
                        detail[3] = True
                        print("purchase successful")
                    else:
                        print("you don't have enough coins to purchase this!")
                print("weapon equipped")

    def _draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        # blit the icons in the top-right corner
        for name in self.icons:
            self.screen.blit(self.icons[name], self.icons_pos[name])
            text_surface = self.small_font.render(str(self.user_fortune[name]), True, Color("tomato"))
            self.screen.blit(text_surface, self.icons_txt_pos[name])

        # blit the goods icons
        for name in self.goods:
            self.screen.blit(self.goods[name], self.goods_pos[name])

        # blit the buttons with text on which that enables user interaction
        for good_type in self.buttons:
            for button in self.buttons[good_type]:
                self.buttons[good_type][button].draw(self.screen, self.small_font)

        pygame.display.update()
