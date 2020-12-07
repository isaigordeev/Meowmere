from game_object import *

pygame.display.set_caption('under_Terraria')

WINDOW_SIZE = (1000, 800)

BACKGROUND_COLOR = (146, 244, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Map(GameObject):
    def __init__(self):
        self.tile_surface = []
        self.game_map = [[]]
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.isay = pygame.image.load('pictures/isay.png')
        self.TILE_SIZE_x = self.isay.get_width()
        self.TILE_SIZE_y = self.isay.get_height()
        self.display = pygame.Surface(WINDOW_SIZE)

    def generation(self):
        for i in range(int(WINDOW_SIZE[1] / self.isay.get_height()) + 1):
            self.game_map.append([])
            for j in range(int(WINDOW_SIZE[0] / self.isay.get_width()) + 1):
                if i < int(WINDOW_SIZE[1] / (2 * self.isay.get_height())):
                    self.game_map[i].append('0')
                else:
                    self.game_map[i].append('1')
        self.game_map[4][10] = '1' #test
        self.game_map[7][3] = '1'
        self.game_map[9][3] = '1'
        self.game_map[10][2] = '0'
        self.game_map[10][1] = '0'



    def print_map_seed(self):
        print(*self.game_map, sep='\n')
    def print_map_seed_by(self):
        for i in range(int(WINDOW_SIZE[1] / self.isay.get_height()) + 1):
                print(*self.game_map[i])

    def building(self, cam_x, cam_y):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    self.display.blit(self.isay, (x * self.TILE_SIZE_x - cam_x, y * self.TILE_SIZE_y - cam_y))
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

