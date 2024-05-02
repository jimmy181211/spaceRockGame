from util import load_sprite, resize_img, print_text_at
from pygame.math import Vector2


class Button:
    def __init__(self, center, label, img_name:str = "button", scale=0.25,txt_pos:tuple=None):
        self.__button = resize_img(load_sprite(img_name), scale)
        self.__button_active = resize_img(self.__button, 1.1)
        # the buttons are static.Hence, the positions don't change
        self.center = Vector2(center)
        self.__button.get_rect().center = self.center
        self.__button_active.get_rect().center = self.center
        self.label = label
        # state controller
        self.is_active = False
        self.radius=self.button.get_width()/2
        if txt_pos is None:
            self.txt_pos=self.center
        else:
            self.txt_pos=txt_pos

    @property
    def button(self):
        return self.__button_active if self.is_active else self.__button

    def collide(self, pos: tuple) -> str:
        if self.center.distance_to(Vector2(pos)) < self.radius:
            self.is_active=True
            return self.label
        self.is_active=False
        return ""

    def draw(self, surface, font=None):
        # display the button
        blit_pos=self.center-Vector2(self.radius)
        surface.blit(self.button,blit_pos)
        if font is not None:
            # display the text label
            print_text_at(surface, self.label, font, self.txt_pos)


class Buttons:
    def __init__(self, entries: dict, bg_size: tuple,):
        self.entry_labels = list(entries.keys())
        self.button_num = len(self.entry_labels)
        # the space for each button
        self.length = bg_size[0] / (self.button_num + 1)
        self.buttons=[]
        for i in range(self.button_num):
            x=self.length * (i + 1)
            y=bg_size[1] / 2 + 100
            self.buttons.append(Button((x,y),self.entry_labels[i],txt_pos=(x,y+150)))

    def collide(self, pos) -> str:
        for button in self.buttons:
            label = button.collide(pos)
            if label!="":
                return label
        return ""

    def draw(self, surface, font):
        for button in self.buttons:
            button.draw(surface, font)
