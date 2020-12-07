import pygame, sys
from pygame.locals import *


class Player:
    def __init__(self):
        self.player_image = pygame.image.load('pictures/tanya_right.png')
        self.moving_right = False
        self.last_side = 0
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.velocity = [0, 0]
        self.step_x = 5
        self.step_y = -15
        self.player_location = [500, 0]
        self.player_y_gravitation = 0
        self.gravity_step_down = 0.3
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(),
                                       self.player_image.get_height())
        self.test_rect = pygame.Rect(500, 100, 100, 50)
        self.air_time = 0
        self.action_dist = 20

    def is_moving_down(self, event):
        if event.key == K_d:
            self.moving_right = True
        if event.key == K_a:
            self.moving_left = True
        if event.key == K_SPACE:
            if self.air_time < 6:
                self.player_y_gravitation = self.step_y

    def is_moving_up(self, event):
        if event.key == K_d:
            self.moving_right = False
            self.velocity[0] = 0
        if event.key == K_a:
            self.moving_left = False
            self.velocity[0] = 0


    def placement(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player_rect.x += self.velocity[0]
        touches = self.touching(tiles)
        for tile in touches:
            if self.velocity[0] > 0:
                self.player_rect.right = tile.left
                self.collision_types['right'] = True
            elif self.velocity[0] < 0:
                self.player_rect.left = tile.right
                self.collision_types['left'] = True
        self.player_rect.y += self.velocity[1]
        touches = self.touching(tiles)
        for tile in touches:
            if self.velocity[1] > 0:
                self.player_rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.velocity[1] < 0:
                self.player_rect.top = tile.bottom
                self.collision_types['top'] = True
        return self.player_rect, self.collision_types

    def touching(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def define_velocity(self):
        if self.moving_right == True:
            self.velocity[0] = self.step_x
        if self.moving_left == True:
            self.velocity[0] = -self.step_x
        self.velocity[1] += self.player_y_gravitation
        self.player_y_gravitation = self.gravity_step_down
        if self.player_y_gravitation > 3:
            self.player_y_gravitation = 3

    def gravitation(self):
        if self.collision_types['bottom'] == True:
            self.air_time = 0
            self.player_y_gravitation = 0
        else:
            self.air_time += 1

    def destroy(self, tiles, event, game_map, TILE_SIZE_x, TILE_SIZE_y):

        for tile in tiles:
            radius = (TILE_SIZE_x/2)
            if (self.player_rect.x - event.pos[0])**2 + (self.player_rect.y - event.pos[1])**2 <= self.action_dist**2:
                if (tile.x + radius/2 - event.pos[0])**2 + ( tile.y + radius/2 - event.pos[1]) ** 2 <= radius ** 2:
                    game_map[int(tile.x/TILE_SIZE_x)][int(tile.y/TILE_SIZE_y)] = '0'