import pygame, sys
from pygame.locals import *

from game_map import RED, GREEN, WINDOW_SIZE


class Mob:
    def __init__(self, mob_location, difficulty):
        self.difficulty = 30 * difficulty
        self.mob_image = pygame.image.load('pictures/ghost.gif')
        self.moving_right = False
        self.last_side = 0
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.velocity = [0, 0]
        self.step_x = 5
        self.step_y = -15
        self.mob_location = mob_location
        self.mob_y_gravitation = 0
        self.gravity_step_down = 0.3
        self.mob_rect = pygame.Rect(self.mob_location[0], self.mob_location[1], self.mob_image.get_width(),
                                    self.mob_image.get_height())
        self.air_time = 0
        self.action_dist = 20
        self.full_hp = 10000
        self.hp = self.full_hp
        self.hp_indicator = 50
        self.full_hp_indicator = self.hp_indicator
        self.heat_hand = 1
        self.alive = True

    def handle_mob(self, tiles, display, player_rect_x, player_rect_y, camera):
        self.drawing(display, camera)
        self.health_mob(display, camera)
        self.define_velocity_mob(player_rect_x, player_rect_y)
        self.placement_mob(tiles)

    def placement_mob(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.mob_rect.x += self.velocity[0]
        # left-right wall enabled
        touches = self.touching_mob(tiles)
        for tile in touches:
            if self.velocity[0] > 0:
                self.mob_rect.right = tile.left
                self.collision_types['right'] = True
            elif self.velocity[0] < 0:
                self.mob_rect.left = tile.right
                self.collision_types['left'] = True
        self.mob_rect.y += self.velocity[1]
        touches = self.touching_mob(tiles)
        for tile in touches:
            if self.velocity[1] > 0:
                self.mob_rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.velocity[1] < 0:
                self.mob_rect.top = tile.bottom
                self.collision_types['top'] = True
        return self.mob_rect, self.collision_types

    def touching_mob(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.mob_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def define_velocity_mob(self, player_rect_x, player_rect_y):
        if abs(player_rect_x - self.mob_rect.x) < 300:
            if player_rect_x - self.difficulty > self.mob_rect.x:
                self.velocity[0] = self.step_x / 2
                self.moving_right = True
                self.moving_left = False
            if player_rect_x + self.difficulty < self.mob_rect.x:
                self.velocity[0] = -self.step_x / 2
                self.moving_left = True
                self.moving_right = False
            # y - axis
            if abs(player_rect_y - self.mob_rect.y) > 100 + self.difficulty:
                self.velocity[1] = -self.step_y / 2
                if abs(player_rect_y - self.mob_rect.y) == 100:
                    self.velocity[1] = 0
            if abs(player_rect_y - self.mob_rect.y) < 100 - self.difficulty:
                self.velocity[1] = +self.step_y / 2
                if abs(player_rect_y - self.mob_rect.y) == 100:
                    self.velocity[1] = 0

    def health_mob(self, display, camera_mob):
        self.red = pygame.Rect(self.mob_rect.x - camera_mob[0] - 10, self.mob_rect.y - camera_mob[1] - 10, self.full_hp_indicator,
                               5)
        self.green = pygame.Rect(self.mob_rect.x - camera_mob[0] - 10, self.mob_rect.y - camera_mob[1] - 10,
                                 self.hp_indicator, 5)
        pygame.draw.rect(display, RED, self.red)
        pygame.draw.rect(display, GREEN, self.green)

    def hit_mob(self, event, camera):
        a = self.hp
        b = self.hp_indicator
        if (self.mob_rect.x - camera[0] - event.pos[0] + self.mob_image.get_width() / 2) ** 2 + (
                self.mob_rect.y - camera[1] - event.pos[1] + self.mob_image.get_height() / 2) ** 2 < 100:
            while self.hp > 0:
                self.hp -= self.heat_hand
                self.hp_indicator -= (self.hp_indicator*self.heat_hand / self.full_hp)
            if self.hp == 0 and a != 0:
                self.hp = a - self.heat_hand
                self.hp_indicator = b - (self.full_hp_indicator*self.heat_hand / self.full_hp)
            if a == 0:
                self.alive = False

    # def beat_player(self, player):
    #     if (self.mob_rect.x - player.player_rect.x )**2  + (self.mob_rect.y - player.player_rect.y )**2 < 300:
    #         player.hp-=

    # def death_mob(self):
    #     if not self.alive:

    def drawing(self, display, camera_speed):
        if self.moving_right:
            display.blit(pygame.transform.flip(self.mob_image, True, False),
                         (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
            self.last_side = 0
        elif self.moving_left:
            display.blit(pygame.transform.flip(self.mob_image, False, False),
                         (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
            self.last_side = 1
        elif not self.moving_right and not self.moving_left:
            if self.last_side == 0:
                display.blit(pygame.transform.flip(self.mob_image, False, False),
                             (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
            elif self.last_side == 1:
                display.blit(pygame.transform.flip(self.mob_image, True, False),
                             (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
