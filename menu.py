import pygame
from game_map import *
from game_map import *


class Menu:
    hovered = False
    clicked = False

    def __init__(self, text, pos, display, menu_font):
        self.text = text
        self.pos = pos
        self.menu_font = menu_font
        self.display = display
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_render()
        self.display.blit(self.render, self.rect)

    def set_render(self):
        self.render = self.menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            if self.clicked:
                return BLACK
            else:
                return BLACK
        else:
            return WHITE

    def set_rect(self):
        self.set_render()
        self.rect = self.render.get_rect()
        self.rect.topleft = self.pos

    def new_window(self, display):
        if self.clicked:
            display.fill(WHITE)
        else:
            pass


def menu_event(options, display):
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
            if pygame.mouse.get_pressed(3) == (1, 0, 0):
                option.clicked = True
                return option.text
            else:
                option.clicked = False
        else:
            option.hovered = False
            option.clicked = False
        option.draw()
        option.new_window(display)
