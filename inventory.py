import pygame, sys
from pygame.locals import *
from game_map import GREY, WINDOW_SIZE, RED


class Inventory:
    def __init__(self, object_image, object_number, inventory_size, inventory_location, identificator):
        self.inventory_location = inventory_location
        self.object = object_image
        self.object_item = 0
        self.object_inventory = False
        self.object_number = object_number
        self.inventory_size = inventory_size
        self.identificator = identificator


    def inventory_define(self):
        if self.object_item > 0:
            self.object_inventory = True
        else:
            self.object_inventory = False

    def object_inventory_show(self, display):
        self.inventory_define()
        if self.object_inventory:
            display.blit(pygame.transform.scale(self.object, (
            int(self.object.get_width() * self.inventory_size), int(self.object.get_height() * self.inventory_size))), (
                         self.inventory_location[0] + (
                                     self.object_number - 1) * self.object.get_width() * self.inventory_size,
                         self.inventory_location[1]))

    def inventory_build(self, event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera, num):
        if num == self.object_number:
            if self.object_inventory:
                if game_map[int((event.pos[1] + camera[1]) / TILE_SIZE_y)][
                    int((event.pos[0] + camera[0]) / TILE_SIZE_x)] == '0':
                    self.object_item -= 1
                    game_map[int((event.pos[1] + camera[1]) / TILE_SIZE_y)][
                        int((event.pos[0] + camera[0]) / TILE_SIZE_x)] = self.identificator
