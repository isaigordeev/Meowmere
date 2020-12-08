from game_map import *
from player import *
from camera import *
from mob import *
clock = pygame.time.Clock()
pygame.init()


Tanya = Player([500, 0])
Isay = Mob([0, 0], 1)
Max = Mob([50, 0], 2)
Ed = Mob([25, 50], 3)
World = Map()
Camera = Camera()
World.map_file_reading('map_seed')

while True:
    World.display.fill(BACKGROUND_COLOR)

    Camera.moving_cam(Tanya.player_rect.x, Tanya.player_rect.y)
    pygame.draw.rect(World.display, (BROWN), pygame.Rect(0 - Camera.scroll_speed[0]
                                                         , 175 - Camera.scroll_speed[1], 1000, 1000))  # cavern background style

    World.building(Camera.scroll_speed)

    Tanya.handle_player(World.tile_surface, World.display, Camera.scroll_speed)
    # Isay.handle_mob(World.tile_surface, World.display, Tanya.player_rect.x, Tanya.player_rect.y, Camera.scroll_speed)
    # Max.handle_mob(World.tile_surface, World.display, Tanya.player_rect.x, Tanya.player_rect.y, Camera.scroll_speed)
    # Ed.handle_mob(World.tile_surface, World.display, Tanya.player_rect.x, Tanya.player_rect.y, Camera.scroll_speed)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            Tanya.is_moving_down(event)
            Tanya.choice_item(event)
        if event.type == KEYUP:
            Tanya.is_moving_up(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Tanya.destroy(World.tile_surface, event, World.game_map, TILE_SIZE_x=World.TILE_SIZE_x,
                              TILE_SIZE_y=World.TILE_SIZE_y, camera=Camera.scroll_speed)
                # print(Tanya.ground_item, Tanya.ground_inventory, Tanya.ground_item, Tanya.num)
            if event.button == 3:
                Tanya.build(World.tile_surface, event, World.game_map, TILE_SIZE_x=World.TILE_SIZE_x,
                              TILE_SIZE_y=World.TILE_SIZE_y, camera=Camera.scroll_speed)


    World.screen.set_alpha(None)
    World.screen.blit(pygame.transform.scale(World.display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
