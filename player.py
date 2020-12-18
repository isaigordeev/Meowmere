import pygame
import sys
from pygame.locals import *
from game_map import GREY, WINDOW_SIZE, RED
from music import *
from inventory import *

pygame.font.init()

class Player:
    '''
    Class is responsible for actions of the player and its interaction with the inventory, the mob and the internal world
    '''
    def __init__(self, player_location):
        self.player_image = pygame.image.load('pictures/santa.png')
        self.moving_right = False
        self.last_side = 0
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.velocity = [0, 0]
        self.step_x = 5
        self.step_y = -5
        self.player_location = player_location
        self.player_y_gravitation = 0
        self.gravity_step_down = 0.5
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(),
                                       self.player_image.get_height())
        self.air_time = 0
        self.action_dist = 8000

        self.inventory_location = [10, 10]
        self.inventory_number_items = 6
        self.inventory_size = 1.3
        self.inventory_rect = pygame.Rect(self.inventory_location[0], self.inventory_location[1],
                                          self.inventory_number_items * self.player_image.get_width() *
                                          self.inventory_size, self.player_image.get_width() *
                                          self.inventory_size)
        self.num = 1

        self.ground = Inventory(pygame.image.load('pictures/inventory/ground2.png'), 3, self.inventory_size,
                                self.inventory_location, '2')
        self.grass = Inventory(pygame.image.load('pictures/inventory/snow.jpg'), 4, self.inventory_size,
                               self.inventory_location, '1')
        self.stone = Inventory(pygame.image.load('pictures/inventory/stone.png'), 5, self.inventory_size,
                               self.inventory_location, '3')
        self.sword = Inventory(pygame.image.load('pictures/inventory/sword.png'), 1,
                               self.inventory_size, self.inventory_location, '4')
        self.hand = Inventory(pygame.image.load('pictures/inventory/mitten.png'), 2,
                              self.inventory_size, self.inventory_location, '5')
        self.sheld = Inventory(pygame.image.load('pictures/inventory/sheld.png'), 6,
                              self.inventory_size, self.inventory_location, '5')
        self.labelFont = pygame.font.SysFont('Italic', 20 * int(self.inventory_size))

        self.full_hp = 100
        self.hp = 100
        self.alive = True
        self.workshop_is_shown = False
        self.workshop_rect = pygame.Rect(self.inventory_location[0],
                                         self.inventory_location[1] + 35 * self.inventory_size,
                                         self.player_image.get_width() * self.inventory_size,
                                         self.player_image.get_width() * self.inventory_size)
        self.mouse = ()
        self.workshop_identificator = 0
        #self.music = Music()
        self.config_items = []

    def handle_player(self, tiles, display, camera_speed, mob_alive):
        '''
        Function is responsible for handling player's actions
        '''
        self.drawing(display, camera_speed)
        self.inventory_and_workshop(display, mob_alive)
        self.define_velocity()
        self.placement(tiles)
        self.gravitation()
        self.craftshop()

    def is_moving_down(self, event):
        '''
        Function is responsible for handling player's movements with pressing keyboard buttons
        '''
        if event.key == K_d:
            self.moving_right = True
        if event.key == K_a:
            self.moving_left = True
        if event.key == K_SPACE:
            # self.velocity[1] = 7
            if self.air_time < 6:
                self.player_y_gravitation = self.step_y

    def is_moving_up(self, event):
        '''
        Function is responsible for handling player's movements with releasing keyboard buttons
        '''
        if event.key == K_d:
            self.moving_right = False
        if event.key == K_a:
            self.moving_left = False

    def placement(self, tiles):
        '''
        Function is responsible for player's movement and checking a touch with the surface
        '''
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
        '''
        Function is responsible for identifying a touch with a player
        '''
        hit_list = []
        for tile in tiles:
            if self.player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def define_velocity(self):
        '''
        Function is responsible for player's velocity
        '''
        self.velocity = [0, 0]
        if self.moving_right:
            self.velocity[0] += self.step_x
        if self.moving_left:
            self.velocity[0] += -self.step_x
        if self.sheld.object_item > 0 and self.num == 6:
            self.velocity[1] += 2*self.player_y_gravitation
            self.player_y_gravitation += 0.1*self.gravity_step_down
        else:
            self.velocity[1] += self.player_y_gravitation
            self.player_y_gravitation += self.gravity_step_down
        if self.player_y_gravitation > 3:
            self.player_y_gravitation = 3

    def gravitation(self):
        '''
        Function is responsible for the player staying at the surface
        '''
        if self.collision_types['bottom']:
            self.air_time = 0
            self.player_y_gravitation = 0
        else:
            self.air_time += 1

    def drawing(self, display, camera_speed):
        '''
        Function is responsible for showing the player on the screen
        '''
        self.player_image = self.player_image.convert_alpha()
        if self.moving_right:
            display.blit(pygame.transform.flip(self.player_image, False, False),
                         (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
            if self.sword.object_inventory and self.num == 1:
                display.blit(pygame.transform.flip(self.sword.object, False, False),
                             (self.player_rect.x - camera_speed[0] + self.sword.object.get_width(),
                              self.player_rect.y - camera_speed[1]))

            if self.sheld.object_inventory and self.num == 6:
                display.blit(pygame.transform.flip(self.sheld.object, True, False),
                             (self.player_rect.x - camera_speed[0] ,
                              self.player_rect.y - camera_speed[1] + self.sheld.object.get_height()*3/5))
            self.last_side = 0
        elif self.moving_left:
            display.blit(pygame.transform.flip(self.player_image, True, False),
                         (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
            if self.sword.object_inventory and self.num == 1:
                display.blit(pygame.transform.flip(self.sword.object, True, False),
                             (self.player_rect.x - camera_speed[0] - self.sword.object.get_width(),
                              self.player_rect.y - camera_speed[1]))
            if self.sheld.object_inventory and self.num == 6:
                display.blit(pygame.transform.flip(self.sheld.object, False, False),
                             (self.player_rect.x - camera_speed[0],
                              self.player_rect.y - camera_speed[1] + self.sheld.object.get_height() * 3 / 5))
            self.last_side = 1
        elif not self.moving_right and not self.moving_left:
            if self.last_side == 0:
                display.blit(pygame.transform.flip(self.player_image, False, False),
                             (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
                if self.sword.object_inventory and self.num == 1:
                    display.blit(pygame.transform.flip(self.sword.object, False, False),
                                 (self.player_rect.x - camera_speed[0] + self.sword.object.get_width(),
                                  self.player_rect.y - camera_speed[1]))
                if self.sheld.object_inventory and self.num == 6:
                    display.blit(pygame.transform.flip(self.sheld.object, True, False),
                                 (self.player_rect.x - camera_speed[0],
                                  self.player_rect.y - camera_speed[1] + self.sheld.object.get_height() * 3 / 5))
            elif self.last_side == 1:
                display.blit(pygame.transform.flip(self.player_image, True, False),
                             (self.player_rect.x - camera_speed[0], self.player_rect.y - camera_speed[1]))
                if self.sword.object_inventory and self.num == 1:
                    display.blit(pygame.transform.flip(self.sword.object, True, False),
                                 (self.player_rect.x - camera_speed[0] - self.sword.object.get_width(),
                                  self.player_rect.y - camera_speed[1]))
                if self.sheld.object_inventory and self.num == 6:
                    display.blit(pygame.transform.flip(self.sheld.object, False, False),
                                 (self.player_rect.x - camera_speed[0],
                                  self.player_rect.y - camera_speed[1] + self.sheld.object.get_height() * 3 / 5))

    def destroy(self, tiles, event, game_map, TILE_SIZE_x, TILE_SIZE_y, camera: []):
        '''
        Function is responsible for destroying blocks in the world by the player and giving
        destroyed blocks to the player (moving them to his inventory)
        '''
        a = self.ground.object_item
        b = self.grass.object_item
        c = self.stone.object_item
        for tile in tiles:
            radius = (TILE_SIZE_x / 2)
            if (self.player_rect.x - camera[0] - event.pos[0] + TILE_SIZE_x / 2) ** 2 + (
                    self.player_rect.y - camera[1] - event.pos[1] + TILE_SIZE_y) ** 2 <= self.action_dist:
                if (tile.x + radius / 2 - camera[0] - event.pos[0]) ** 2 + (
                        tile.y + radius / 2 - camera[1] - event.pos[1]) ** 2 <= radius ** 2:
                    # self.music.break_music()
                    # self.music.main_music()
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
        '''
        Function is responsible for building with blocks in the world by the player and taking
        set blocks to the player (moving them from his inventory)
        '''
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

    def define_workshop(self, object):
        '''
        Function is responsible for showing items in the workshop and crafting in it
        '''
        if object.moving:
            if ((self.workshop_rect.x + 14) * self.inventory_size - self.mouse[0]) ** 2 + (
                    (self.workshop_rect.y + self.player_image.get_height() / 2 - 11) * self.inventory_size -
                    self.mouse[1]) ** 2 < 75 * self.inventory_size:
                object.object_workshop = True
                self.workshop_identificator = object.identificator
                while object.object_item > 0:
                    object.object_workshop_item += 1
                    object.object_item -= 1

    def inventory_and_workshop(self, display, mob_alive):
        '''
        Function is responsible for showing inventory, items in the inventory, items in the workshop and
        the process of choosing the items in the inventory
        '''
        pygame.draw.rect(display, (GREY), self.inventory_rect)

        if self.workshop_is_shown:
            pygame.draw.rect(display, GREY, self.workshop_rect)
            self.define_workshop(self.ground)
            self.define_workshop(self.grass)
            self.define_workshop(self.stone)

            if self.ground.object_workshop:
                self.ground.object_workshop_show(display)
                self.ground.object_item_workshop_show(display, self.labelFont)
            if not self.ground.object_workshop:
                pygame.draw.rect(display, GREY, self.workshop_rect)

            if self.stone.object_workshop:
                self.stone.object_workshop_show(display)
                self.stone.object_item_workshop_show(display, self.labelFont)
            if not self.stone.object_workshop:
                pygame.draw.rect(display, GREY, self.workshop_rect)

            if self.grass.object_workshop:
                self.grass.object_workshop_show(display)
                self.grass.object_item_workshop_show(display, self.labelFont)
            if not self.grass.object_workshop:
                pygame.draw.rect(display, GREY, self.workshop_rect)

        self.ground.object_inventory_show(display)
        self.grass.object_inventory_show(display)
        self.stone.object_inventory_show(display)
        self.sword.object_inventory_show(display)
        self.hand.object_item = 1
        self.hand.object_inventory_show(display)
        if not mob_alive:
            self.sheld.object_item = 1
            self.sheld.object_inventory_show(display)

        pygame.draw.rect(display, RED, pygame.Rect(
            self.inventory_location[0] + (self.num - 1) * self.player_image.get_width() * self.inventory_size,
            self.inventory_location[1],
            self.player_image.get_width() * self.inventory_size,
            self.player_image.get_width() * self.inventory_size), 3)

        for object_number in range(self.inventory_number_items + 1):
            display.blit(self.labelFont.render(str(object_number), False, BLACK), (
                self.inventory_location[0] +
                ((object_number - 1) * self.player_image.get_width() + 3) * self.inventory_size,
                self.inventory_location[1] + 1 * self.inventory_size))

            self.ground.object_item_show(display, object_number, self.labelFont)
            self.stone.object_item_show(display, object_number, self.labelFont)
            self.grass.object_item_show(display, object_number, self.labelFont)

    def inventory_item_movement(self, event, object):
        '''
        Function is responsible for moving items from the inventory to the workshop
        '''
        if object.object_inventory:
            if (self.inventory_location[0] + (
                    (object.object_number - 1) * self.player_image.get_width() + 14) * self.inventory_size -
                event.pos[0]) ** 2 + (
                    (self.inventory_location[1] + self.player_image.get_height() / 2 - 11) * self.inventory_size -
                    event.pos[1]) ** 2 < 75 * self.inventory_size:
                object.moving = True

    def workshop(self, event):
        '''
        Function is responsible for activating the workshop by the player
        '''
        if event.key == K_e:
            if not self.workshop_is_shown:
                self.workshop_is_shown = True
            else:
                self.workshop_is_shown = False

    def object_inventory_moving(self, event, display, object):
        '''
        Function is responsible for showing items moving from the inventory to the workshop
        '''
        if object.object_inventory and object.moving:
            display.blit(pygame.transform.scale(object.object, (
                int(object.object.get_width() * self.inventory_size),
                int(object.object.get_height() * self.inventory_size))), (
                             event.pos[0],
                             event.pos[1]))

    def drop_item(self, event, object):
        '''
        Function is responsible for activating a drop of the items
        '''
        if event.key == K_q:
            object.object_item = 0
            self.define_workshop(object)

    def drop_items(self, event):
        '''
        Function is responsible for dropping the items by the player
        '''
        if self.num == 3:
            self.drop_item(event, self.ground)
        if self.num == 4:
            self.drop_item(event, self.grass)
        if self.num == 5:
            self.drop_item(event, self.stone)
        if self.num == 1:
            self.drop_item(event, self.sword)
        if self.num == 6:
            self.drop_item(event, self.sheld)

    def craftshop(self):
        '''
        Function is responsible for crafting receipts
        '''
        if self.workshop_identificator == self.ground.identificator:
            if self.ground.object_workshop_item >= 3:
                while self.ground.object_workshop_item >= 3:
                    self.grass.object_item += 1
                    self.ground.object_workshop_item -= 3
            self.ground.object_item += self.ground.object_workshop_item
            self.ground.object_workshop = False
            self.ground.object_workshop_item = 0

        if self.workshop_identificator == self.grass.identificator:
            if self.grass.object_workshop_item >= 1:
                while self.grass.object_workshop_item >= 1:
                    self.ground.object_item += 3
                    self.grass.object_workshop_item -= 1
            self.grass.object_item += self.grass.object_workshop_item
            self.grass.object_workshop = False
            self.grass.object_workshop_item = 0

        if self.workshop_identificator == self.stone.identificator:
            if self.stone.object_workshop_item >= 5:
                while self.stone.object_workshop_item >= 5:
                    self.sword.object_item = 1
                    self.sword.inventory_define()
                    self.stone.object_workshop_item -= 5
            self.stone.object_item += self.stone.object_workshop_item
            self.stone.object_workshop = False
            self.stone.object_workshop_item = 0

    def config_reading(self, path):
        f = open(path+'.txt')
        self.data = f.read()
        f.close()
        self.data = self.data.split(' ')
        for row in self.data:
            self.config_items.append(row)
        self.get_config_items()
    
    def get_config_items(self):
        self.sword.object_item = int(self.config_items[0])
        self.ground.object_item = int(self.config_items[1])
        self.grass.object_item = int(self.config_items[2])
        self.stone.object_item = int(self.config_items[3])

    def config_writing(self, path):
        config_items = ''
        config_items += str(self.sword.object_item)
        config_items += str(self.ground.object_item)
        config_items += str(self.grass.object_item)
        config_items += str(self.stone.object_item)
        f = open(path+'.txt', 'w')
        for i in range(4):
            f.write(config_items[i] + ' ')
        f.close()

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
