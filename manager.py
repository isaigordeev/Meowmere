from game_map import *
from player import *

clock = pygame.time.Clock()
pygame.init()

Tanya = Player()
World = Map()
World.generation()


# World.print_map_seed()


def touching(tiles):
    touches = []
    for tile in tiles:
        if Tanya.player_rect.colliderect(tile):
            touches.append(tile)
    return touches



while True:
    World.screen.fill(BACKGROUND_COLOR)
    World.building()
    World.screen.blit(Tanya.player_image, (Tanya.player_rect.x, Tanya.player_rect.y))
    Tanya.define_velocity()
    Tanya.placement(World.tile_surface)
    Tanya.gravitation()



    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            Tanya.is_moving_down(event)
        if event.type == KEYUP:
            Tanya.is_moving_up(event)
    pygame.display.update()
    clock.tick(60)