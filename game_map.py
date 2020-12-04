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

    def print_map_seed(self):
        print(*self.game_map, sep='\n')

    def building(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    self.screen.blit(self.isay, (x * self.TILE_SIZE_x, y * self.TILE_SIZE_y))
                if tile != '1':
                    self.tile_surface.append(
                        pygame.Rect(x * self.TILE_SIZE_x, y * self.TILE_SIZE_y, self.TILE_SIZE_y, self.TILE_SIZE_x))
                x += 1
            y += 1
