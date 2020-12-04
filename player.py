from game_map import WINDOW_SIZE
from game_object import *


class Player:
    def __init__(self):
        self.player_image = pygame.image.load('pictures/tanya.jpeg')

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.velocity = [0, 0]
        self.step = 5
        self.player_location = [500, 50]
        self.player_y_gravitation = 0
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(),
                                       self.player_image.get_height())
        self.test_rect = pygame.Rect(100, 100, 100, 50)
        self.air_time = 0

    def moving(self):
        if self.moving_right:
            self.player_rect.x += self.step
        if self.moving_left:
            self.player_rect.x -= self.step
        if self.moving_up:
            self.player_rect.y -= self.step * 4
            self.air_time += 1
            if self.air_time > 5:
                self.air_time = 0
                self.moving_up = False

    def is_moving_down(self, event):
        if event.key == K_RIGHT:
            self.moving_right = True
        if event.key == K_LEFT:
            self.moving_left = True
        if event.key == K_UP:
            self.moving_up = True

    def is_moving_up(self, event):
        if event.key == K_RIGHT:
            self.moving_right = False
        if event.key == K_LEFT:
            self.moving_left = False

    def touching(self, tiles):
        touches = []
        for tile in tiles:
            if self.player_rect.colliderect(tile):
                touches.append(tile)
        return touches

    def gravitation(self):
        if self.collision_types['bottom']:
            self.player_y_gravitation = 0
            self.air_time = 0
        else:
            self.player_y_gravitation = 2
            self.air_time += 1
        self.player_rect.y += self.player_y_gravitation

    def walking_ground(self, tiles):
        self.collision_types = {'bottom': False, 'top': False, 'right': False, 'left': False}
        touches = self.touching(tiles)
        for tile in touches:
            if self.player_y_gravitation > 0:
                self.player_rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.player_y_gravitation < 0:
                self.player_rect.top = tile.bottom
                self.collision_types['top'] = True

