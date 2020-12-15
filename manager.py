
from game_map import *
from player import *
from camera import *
from mob import *
from music import *
import random_map 
clock = pygame.time.Clock()
pygame.init()


Tanya = Player([200, 0])

Isay = Mob([0, 0], 1)
Max = Mob([50, 0], 2)
Ed = Mob([25, 50], 3)
World = Map()
Camera_mob = Camera()
Camera = Camera()
Music = Music()
random_map.create_map()
World.map_file_reading('map_seed')
Tanya.player_image.convert()
Tanya.player_image.set_colorkey((255, 255, 255))


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = Tanya.labelFont.render(fps, 1, pygame.Color(RED))
    return fps_text


Music.music()

while True:
    World.display.fill(BACKGROUND_COLOR)

    Camera.moving_cam(Tanya.player_rect.x, Tanya.player_rect.y)
    Max.handle_mob(World.tile_surface, World.display, Tanya.player_rect.x, Tanya.player_rect.y, Camera.scroll_speed)
    Camera_mob.moving_cam(Max.mob_rect.x, Max.mob_rect.y)
    pygame.draw.rect(World.display, (BROWN), pygame.Rect(0 - Camera.scroll_speed[0]
                                                         , 175 - Camera.scroll_speed[1], 1000, 1000))  # cavern background style

    World.building(Camera.scroll_speed)

    Tanya.handle_player(World.tile_surface, World.display, Camera.scroll_speed)
    World.display.blit(update_fps(), (300, 0))


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            Tanya.is_moving_down(event)
            Tanya.choice_item(event)
            Tanya.workshop(event)
        if event.type == KEYUP:
            Tanya.is_moving_up(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Tanya.destroy(World.tile_surface, event, World.game_map, TILE_SIZE_x=World.TILE_SIZE_x,
                              TILE_SIZE_y=World.TILE_SIZE_y, camera=Camera.scroll_speed)
                Max.hit_mob(event, Camera.scroll_speed, Tanya.num, Tanya.sword.object_inventory)
                Tanya.inventory_item_movement(event, Tanya.ground)
                Tanya.inventory_item_movement(event, Tanya.grass)
                Tanya.inventory_item_movement(event, Tanya.stone)

            if event.button == 3:
                Tanya.build(World.tile_surface, event, World.game_map, TILE_SIZE_x=World.TILE_SIZE_x,
                              TILE_SIZE_y=World.TILE_SIZE_y, camera=Camera.scroll_speed)
        if event.type == pygame.MOUSEMOTION:
            Tanya.mouse = event.pos
            if event.buttons[0]:
                Tanya.object_inventory_moving(event, World.display, Tanya.ground)
                Tanya.object_inventory_moving(event, World.display, Tanya.grass)
                Tanya.object_inventory_moving(event, World.display, Tanya.stone)

            if not event.buttons[0]:
                Tanya.ground.moving = False
                Tanya.grass.moving = False
                Tanya.stone.moving = False



    World.screen.set_alpha(None)
    World.screen.blit(World.display, (0, 0))
    # pygame.display.flip()
    pygame.display.update()
    clock.tick(60)