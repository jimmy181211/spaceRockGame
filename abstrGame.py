from abc import ABC, abstractmethod
import pygame
from util import load_sprite


class AbstrGame(ABC):
    def __init__(self,bg_img_name,page_name="page"):
        self.keep_going=True
        self.bg_w = 800
        self.bg_h = 600
        self.page_name=page_name
        self.screen = pygame.display.set_mode((self.bg_w, self.bg_h))
        self._init_pygame()

        self.keep_going = True
        self.font=pygame.font.Font(None,64)
        self.bg_img = load_sprite(bg_img_name, False)
        self.clock = pygame.time.Clock()

    def main_loop(self):
        pygame.key.stop_text_input()
        while self.keep_going:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        self.screen.fill((0, 0, 255))
        pygame.display.set_caption(self.page_name)

    def _quit(self):
        self.keep_going=False

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._quit()

    @abstractmethod
    def _process_game_logic(self):
        pass

    @abstractmethod
    def _draw(self):
        pass
