from shop import Shop
from game import SpaceRocks
import pygame
from abstrGame import AbstrGame
from util import is_num
import time
from msg_box import MsgBox
from button import Buttons
from shield import ShieldType
from bullet import BulletType


class MainPage(AbstrGame):
    def __init__(self, info: tuple):
        super().__init__("mainpage", "main page")
        self.user_info = {"username": info[0],
                          "email": info[2]
                          }
        self.user_fortune = {
            "coin_num": info[3],
            "bullet_type": BulletType(info[4]),
            "shield_num": info[5],
            "shield_type": ShieldType(info[6])
        }
        self.entry_comps = {"shop": Shop(self.user_info, self.user_fortune), "game": SpaceRocks()}
        self.button_comp = Buttons(self.entry_comps, (self.bg_w, self.bg_h))
        self.clicked_sound = [pygame.mixer.Sound("sound/button_clicked.wav"), False]
        # load sounds. The second element shows whether it's played or not
        self.touched_sound = [pygame.mixer.Sound("sound/button_touched.wav"), False]
        # coin_num and shield_num can be changed in the game
        self.msg_box = MsgBox(["coin_num", "shield_num"])

    @staticmethod
    def play(sound):
        if not sound[1]:
            sound[0].play()
            sound[1] = True

    @staticmethod
    def enable_play(sound):
        if sound[1]:
            sound[1] = False

    def _process_game_logic(self):
        pass

    def button_clicked(self,page_label):
        print("hello")
        self.play(self.clicked_sound)
        time.sleep(0.5)

        if page_label == "game":
            # equipment before the game
            self.msg_box.show()
            time.sleep(0.1)
            # a copy of the user fortune
            params = {key: self.user_fortune[key] for key in self.user_fortune}

            for label in self.msg_box.result_list:
                num = self.msg_box.result_list[label]
                if is_num(num) and int(num) > 0:
                    # if the user is entering more that what he has
                    if int(num) >= self.user_fortune[label]:
                        params[label] = self.user_fortune[label]
                        self.user_fortune[label] = 0
                    else:
                        params[label] = int(num)
                        self.user_fortune[label] -= int(num)
                # default setting
                else:
                    params[label] = 0
            self.entry_comps["game"].params = params

        page = self.entry_comps[page_label]
        page.main_loop()
        if page_label == "game":
            self.msg_box = MsgBox(["coin_num", "shield_num"])
            if page.is_win:
                self.user_fortune["coin_num"] += page.params.coin_num
            # create a new game page object
            self.entry_comps[page_label] = SpaceRocks()

        elif page_label == "shop":
            # update the user_fortune
            self.user_fortune = page.user_fortune
            self.entry_comps[page_label] = Shop(self.user_info, self.user_fortune)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._quit()

            # detect whether the mouse collides with the button
            page_label = self.button_comp.collide(pygame.mouse.get_pos())

            # is the button clicked
            if event.type == pygame.MOUSEBUTTONDOWN and page_label != "":
                self.button_clicked(page_label)

            # is the button is touched
            elif page_label != "":
                self.play(self.touched_sound)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.enable_play(self.clicked_sound)

            elif page_label == "":
                self.enable_play(self.touched_sound)

    def _draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.button_comp.draw(self.screen, self.font)
        pygame.display.update()
        self.clock.tick(60)
