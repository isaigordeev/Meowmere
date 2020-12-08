from game_object import *

pygame.display.set_caption('under_Terraria')

WINDOW_SIZE = (500, 400)

BACKGROUND_COLOR = (146, 244, 255)
BROWN = (125,75,0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Map(GameObject):
    def __init__(self):
        self.tile_surface = []
        self.game_map = [[]]
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.grass = pygame.image.load('pictures/ground1.png')
        self.ground =  pygame.image.load('pictures/ground2.png')
        self.TILE_SIZE_x = self.grass.get_width()
        self.TILE_SIZE_y = self.grass.get_height()
        self.display = pygame.Surface(WINDOW_SIZE)

    def generation(self):
        for i in range(int(WINDOW_SIZE[1] / self.grass.get_height()) + 1):
            self.game_map.append([])
            for j in range(int(WINDOW_SIZE[0] / self.grass.get_width()) + 1):
                if i < int(WINDOW_SIZE[1] / (2 * self.grass.get_height())):
                    self.game_map[i].append('0')
                else:
                    self.game_map[i].append('1')



    def print_map_seed(self):
        print(*self.game_map, sep='\n')
    def print_map_seed_by(self):
        for i in range(int(WINDOW_SIZE[1] / self.grass.get_height()) + 1):
                print(*self.game_map[i])

    def building(self, camera):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    self.display.blit(self.grass, (x * self.TILE_SIZE_x - camera[0], y * self.TILE_SIZE_y - camera[1]))
                if tile == '2':
                    self.display.blit(self.ground, (x * self.TILE_SIZE_x - camera[0], y * self.TILE_SIZE_y - camera[1]))
                if tile != '0':
                    self.tile_surface.append(
                        pygame.Rect(x * self.TILE_SIZE_x, y * self.TILE_SIZE_y, self.TILE_SIZE_x, self.TILE_SIZE_y))
                x += 1
            y += 1

    def map_file_reading(self, path):
        f = open(path+'.txt')
        self.data = f.read()
        f.close()
        self.data = self.data.split('\n')
        for row in self.data:
            self.game_map.append(list(row))