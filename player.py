from game_map import WINDOW_SIZE
from game_object import *


class Player:
    def __init__(self):
        self.player_image = pygame.image.load('pictures/tanya.jpeg')

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.step = 6
        self.player_location = [50, 50]
        self.player_y_gravitation = 0

        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_image.get_width(),
                                       self.player_image.get_height())
        self.test_rect = pygame.Rect(100, 100, 100, 50)

    def moving(self):
        if self.moving_right:
            self.player_location[0] += self.step
        if self.moving_left:
            self.player_location[0] -= self.step
        if self.moving_up:
            self.player_location[1] -= self.step
        if self.moving_down:
            self.player_location[1] += self.step

    def is_moving_up(self, event):
        if event.key == K_RIGHT:
            self.moving_right = True
        if event.key == K_LEFT:
            self.moving_left = True
        if event.key == K_UP:
            self.moving_up = True
        if event.key == K_DOWN:
            self.moving_down = True

    def is_moving_down(self, event):
        if event.key == K_RIGHT:
            self.moving_right = False
        if event.key == K_LEFT:
            self.moving_left = False
        if event.key == K_UP:
            self.moving_up = False
        if event.key == K_DOWN:
            self.moving_down = False
    
    def gravitation(self):
        if self.player_location[1] > WINDOW_SIZE[1] - self.player_image.get_height():
            self.player_y_gravitation = 0
        else:
            self.player_y_gravitation =+ 1
        self.player_location[1] += self.player_y_gravitation
