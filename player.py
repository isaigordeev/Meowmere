import pygame, sys
from pygame.locals import *
from game_map import GREY, WINDOW_SIZE, RED
from inventory import *
pygame.font.init()

class Player:
    def __init__(self, player_location):
        self.player_image = pygame.image.load('pictures/tanya_right.png')
        self.moving_right = False
        self.last_side = 0
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.velocity = [0, 0]
        self.step_x = 5
        self.step_y = -15
        self.player_location = player_location
        self.player_y_gravitation = 0
        self.gravity_step_down = 0.3
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(),
                                       self.player_image.get_height())
        self.air_time = 0
        self.action_dist = 8000

        self.inventory_location = [10, 10]
        self.inventory_number_items = 6
        self.inventory_size = 1.5
        self.inventory_rect = pygame.Rect(self.inventory_location[0], self.inventory_location[1],
                                          self.inventory_number_items * self.player_image.get_width() * self.inventory_size,
                                          self.player_image.get_width() * self.inventory_size)
        self.num = 1

        self.ground = Inventory(pygame.image.load('pictures/inventory/ground2.png'), 4, self.inventory_size, self.inventory_location, '2')
        self.grass = Inventory(pygame.image.load('pictures/inventory/ground1.png'), 5, self.inventory_size, self.inventory_location, '1')
        self.stone = Inventory(pygame.image.load('pictures/inventory/stone.png'), 6, self.inventory_size, self.inventory_location, '3')
        self.labelFont = pygame.font.SysFont('Italic', 20*int(self.inventory_size))

    def handle_player(self, tiles, display, camera_speed):
        self.drawing(display, camera_speed)
        self.inventory(display)
        self.define_velocity()
        self.placement(tiles)
        self.gravitation()

    def is_moving_down(self, event):
        if event.key == K_d:
            self.moving_right = True
        if event.key == K_a:
            self.moving_left = True
        if event.key == K_SPACE:
            self.velocity[1] = 7
            if self.air_time < 6:
                self.player_y_gravitation = self.step_y

    def is_moving_up(self, event):
        if event.key == K_d:
            self.moving_right = False
            self.velocity[0] = 0
        if event.key == K_a:
            self.moving_left = False
            self.velocity[0] = 0
        if event.key == K_SPACE:
            self.velocity[1] = 1

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

    def drawing(self, display, camera_speed):
        self.player_image = self.player_image.convert_alpha()
        if self.moving_right:
            display.blit(pygame.transform.flip(self.player_image, False, False),
                         (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
            self.last_side = 0
        elif self.moving_left:
            display.blit(pygame.transform.flip(self.player_image, True, False),
                         (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
            self.last_side = 1
        elif not self.moving_right and not self.moving_left:
            if self.last_side == 0:
                display.blit(pygame.transform.flip(self.player_image, False, False),
                             (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
            elif self.last_side == 1:
                display.blit(pygame.transform.flip(self.player_image, True, False),
                             (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))

    def destroy(self, tiles, event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera: []):
        a = self.ground.object_item
        b = self.grass.object_item
        c = self.stone.object_item
        for tile in tiles:
            radius = (TILE_SIZE_x / 2)
            if (self.player_rect.x - camera[0] - event.pos[0] + TILE_SIZE_x / 2) ** 2 + (
                    self.player_rect.y - camera[1] - event.pos[1] + TILE_SIZE_y) ** 2 <= self.action_dist:
                if (tile.x + radius / 2 - camera[0] - event.pos[0]) ** 2 + (
                        tile.y + radius / 2 - camera[1] - event.pos[1]) ** 2 <= radius ** 2:
                    tiles.remove(tile)
                    if game_map[int((event.pos[1] + camera[1]) / TILE_SIZE_y)][
                        int((event.pos[0] + camera[0]) / TILE_SIZE_x)] == self.ground.identificator:
                        self.ground.object_item += 1
                        if self.ground.object_item - a > 1:
                            self.ground.object_item = a + 1
                        game_map[int(tile.y / TILE_SIZE_y)][int(tile.x / TILE_SIZE_x)] = '0'
                    if game_map[int((event.pos[1] + camera[1]) / TILE_SIZE_y)][
                        int((event.pos[0] + camera[0]) / TILE_SIZE_x)] == self.grass.identificator:
                        self.grass.object_item += 1
                        if self.grass.object_item - b > 1:
                            self.grass.object_item = b + 1
                        game_map[int(tile.y / TILE_SIZE_y)][int(tile.x / TILE_SIZE_x)] = '0'
                    if game_map[int((event.pos[1] + camera[1]) / TILE_SIZE_y)][
                        int((event.pos[0] + camera[0]) / TILE_SIZE_x)] == self.stone.identificator:
                        self.stone.object_item += 1
                        if self.stone.object_item - c > 1:
                            self.stone.object_item = c + 1
                        game_map[int(tile.y / TILE_SIZE_y)][int(tile.x / TILE_SIZE_x)] = '0'


    def build(self, tiles, event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera: []):
        self.ground.inventory_define()
        self.grass.inventory_define()
        self.stone.inventory_define()
        if (self.player_rect.x - camera[0] - event.pos[0] + TILE_SIZE_x / 2) ** 2 + (
                self.player_rect.y - camera[1] - event.pos[1] + TILE_SIZE_y) ** 2 <= self.action_dist:
            self.ground.inventory_build(event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera, self.num)
            self.grass.inventory_build(event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera, self.num)
            self.stone.inventory_build(event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera, self.num)
            tiles.append(pygame.Rect(int((event.pos[1] + camera[1]) / TILE_SIZE_y) * TILE_SIZE_x,
                                     int((event.pos[0] + camera[0]) / TILE_SIZE_x) * TILE_SIZE_y, TILE_SIZE_x,
                                     TILE_SIZE_y))


    def inventory(self, display):
        pygame.draw.rect(display, (GREY), self.inventory_rect)
        self.ground.object_inventory_show(display)
        self.grass.object_inventory_show(display)
        self.stone.object_inventory_show(display)
        pygame.draw.rect(display, RED, pygame.Rect(
            self.inventory_location[0] + (self.num - 1) * self.player_image.get_width() * self.inventory_size,
            self.inventory_location[1],
            self.player_image.get_width() * self.inventory_size,
            self.player_image.get_width() * self.inventory_size), 3)
        for object_number in range(self.inventory_number_items+1):
            display.blit(self.labelFont.render(str(object_number), False, BLACK), (
                self.inventory_location[0] + ((
                        object_number - 1) * self.player_image.get_width()+3) * self.inventory_size,
                self.inventory_location[1]+1 * self.inventory_size,))
    def choice_item(self, event):
        if event.key == K_1:
            self.num = 1
        if event.key == K_2:
            self.num = 2
        if event.key == K_3:
            self.num = 3
        if event.key == K_4:
            self.num = 4
        if event.key == K_5:
            self.num = 5
        if event.key == K_6:
            self.num = 6
