from pygame.image import load
from pygame.math import Vector2
import random
import pygame
from pygame import Color
from pygame.mixer import Sound
import threading
import math

def load_sprite(name,with_alpha=True):
    path=f"sprite/{name}.png"
    loaded_sprite=load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_pos(pos,surface):
    x,y=pos
    w,h=surface.get_size()
    return Vector2(x%w,y%h)


def get_rand_velocity(min_speed,max_speed):
    speed=random.randint(min_speed,max_speed)
    ang=random.randint(0,360)
    return Vector2((speed,0)).rotate(ang)


def is_num(num:str):
    for char in num:
        if not 48<=ord(char)<=57:
            return False
    return True


def rand_pos(surface):
    ##########
    return Vector2(random.randrange(surface.get_width()),random.randrange(surface.get_width()))


def load_sound(name):
    path=f"sound/{name}.wav"
    return Sound(path)


def print_text(surface,text,font,color=Color("tomato")):
    text_surface=font.render(text,True,color)
    rect=text_surface.get_rect()
    rect.center=Vector2(surface.get_size())/2
    #blit the text
    surface.blit(text_surface,rect)


def print_text_at(surface,text,font,pos,color=Color("tomato")):
    text_surface=font.render(text,True,color)
    rect=text_surface.get_rect()
    rect.center=pos
    surface.blit(text_surface,rect)


def timer(time:int,func):
    if time>0:
        th1=threading.Timer(1,timer,(time-1,func))
        th1.start()
    else:
        func()

def resize_img(img_obj,scale=1):
    return pygame.transform.scale(img_obj,(img_obj.get_width()*scale,img_obj.get_height()*scale))


def vec_size(vec:Vector2):
    return math.sqrt(vec.x**2+vec.y**2)


def lower_case(string:str):
    result_str=""
    for char in string:
        if 65<=ord(char)<=90:
            result_str+=chr(ord(char)+32)
        else:
            result_str+=char
    return result_str

if __name__=="__main__":
    print(lower_case("maIN"))