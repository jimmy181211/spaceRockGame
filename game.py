import pygame
from util import *
from spaceship import SpaceShip
from asteroid import Asteroid
from abstrGame import AbstrGame
from pygame.mixer import Sound
from coin import Coin


class SpaceRocks(AbstrGame):
    MIN_ASTEROID_DIST = 250

    def __init__(self):
        super().__init__("space", "spacerock")

        # initialise game objects
        self.bullets = []
        self.spaceship = SpaceShip((20, self.bg_h / 2), self.bullets.append, surface=self.screen)
        self.asteroid_num = 4
        self.asteroids = []
        self.coins = []

        # load music
        pygame.mixer.init()
        pygame.mixer.music.load("sound/bg_music.mp3")
        self.banged = Sound("sound/rockBanged.mp3")
        self.crashed = Sound("sound/rockCrashed.mp3")
        self.collect_coin = Sound("sound/collect_coin.wav")

        # initialising the asteroids
        for _ in range(self.asteroid_num):
            while True:
                pos = rand_pos(self.screen)
                if pos.distance_to(self.spaceship.pos) > self.MIN_ASTEROID_DIST:
                    break
            self.asteroids.append(Asteroid(pos, self.asteroids.append, surface=self.screen))

        # miscellaneous
        self.msg = ""  # output message whether the user wins or loses
        icons = {"live_num": ("blood", 0.05), "coin_num": ("coin", 0.05), "shield_num": ("shield_icon", 0.05),
                 "bullet_num": ("bullet_icon", 0.03)}
        self.icons = {name: resize_img(load_sprite(icons[name][0]), icons[name][1]) for name in icons}
        # the permanent positions of the icons on the screen
        self.intv = 10
        self.pos_icons = {}  # position for the icons
        self.pos_txts = {}  # position for the values displayed
        acc_icon = 0
        for cnt, label in enumerate(self.icons):
            img = self.icons[label]
            self.pos_icons[label] = (700, acc_icon + cnt * self.intv)
            self.pos_txts[label] = (700 + self.intv + img.get_width(), acc_icon + cnt * self.intv)
            acc_icon += img.get_height()

        self.small_font = pygame.font.Font(None, 32)
        self.is_win = False
        self.__params = None

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params: dict):
        #the start up number of bullets
        params["bullet_num"] = 5
        self.__params = params
        self.spaceship.params = params

    def main_loop(self):
        pygame.mixer.music.play()
        super().main_loop()

    @staticmethod
    def purchase(func):
        is_succeed = func()
        if not is_succeed:
            print("purchase not successful:not enough coins")
        else:
            print("purchase successful")

    @staticmethod
    def use_skill(func):
        is_succeed=func()
        if not is_succeed:
            print("not enough skills!")
        else:
            print("skill used")

    def _handle_input(self) -> None:
        if not self.spaceship:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._quit()
            elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                SpaceRocks.use_skill(self.spaceship.shoot)
            # shielding mode
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                # protection for 2 seconds
                SpaceRocks.use_skill(self.spaceship.start_shield)
            # buy shields
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                print("buy shields")
                SpaceRocks.purchase(self.spaceship.add_shield)
            # buy bullets
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                print("buy bullets")
                SpaceRocks.purchase(self.spaceship.add_bullet)

        if not self.spaceship:
            return

        is_key_pressed = pygame.key.get_pressed()
        is_left = is_key_pressed[pygame.K_LEFT]
        is_right = is_key_pressed[pygame.K_RIGHT]
        # rotate the spaceship
        if is_left or is_right:
            clockwise = True
            if is_left:
                clockwise = False
            self.spaceship.rotate(clockwise=clockwise)

        # move the spaceship
        if is_key_pressed[pygame.K_UP]:
            self.spaceship.acc()

    def _is_obstacle_die(self,obstacles:list,obstacle):
        if not obstacle.is_die:
            return
        self.crashed.play()
        obstacles.remove(obstacle)
        obstacle.split()
        # add the coins
        for i in range(obstacle.lives):
            self.coins.append(Coin(self.screen, game_obj=obstacle))

    def _process_game_logic(self):
        for game_obj in self._get_game_objects():
            game_obj.move()

        # if the spaceship doesn't exist:
        if not self.spaceship:
            return

        # determine if the spaceship is collided with asteroid
        for asteroid in self.asteroids:
            if asteroid.collide(self.spaceship) or self.spaceship.shield.shield_collide(asteroid):
                self.banged.play()
                self._is_obstacle_die(self.asteroids,asteroid)

            # lost the game
            if self.spaceship.is_die:
                self.spaceship = None
                self.msg = "you lost!"
                # quit the entire game logic in 2 seconds
                timer(2, self._quit)
                break

        # if the spaceship doesn't exist:
        if not self.spaceship:
            return

        # if the spaceship collides with coins
        for coin in self.coins[:]:
            if coin.collide(self.spaceship):
                self.collect_coin.play()
                self.coins.remove(coin)
                # add coins
                self.spaceship.params["coin_num"] += 1

        # if the bullets collide with the asteroid
        for bullet in self.bullets[:]:
            # if the bullets are out of screen, remove the bullets
            if not self.screen.get_rect().collidepoint(bullet.pos):
                self.bullets.remove(bullet)
            for asteroid in self.asteroids[:]:
                asteroid.collide(bullet)
                self._is_obstacle_die(self.asteroids, asteroid)
                if bullet.is_die:
                    self.banged.play()
                    self.bullets.remove(bullet)
                    break

        # win the game
        if not self.asteroids and self.spaceship:
            self.msg = "you won!"
            self.is_win = True
            timer(2, self._quit)

    def _draw(self):
        self.screen.blit(self.bg_img, (0, 0))
        # draw the game_objects
        for game_obj in self._get_game_objects():
            game_obj.draw()

        # draw the messages
        if self.msg:
            print_text(self.screen, self.msg, self.font)

        # draw the equipment bars
        for cnt, label in enumerate(self.icons):
            # symbol
            self.screen.blit(self.icons[label], self.pos_icons[label])
            # value
            if label == "live_num":
                content = self.spaceship.curr_lives if self.spaceship else 0
            else:
                content = self.params[label]
            text_surface = self.small_font.render(str(content), True, Color("tomato"))
            self.screen.blit(text_surface, self.pos_txts[label])

        pygame.display.update()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objs = [*self.asteroids, *self.bullets, *self.coins]
        if self.spaceship:
            game_objs.append(self.spaceship)
        return game_objs
