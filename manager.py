from game_map import *
from player import *
from camera import *
from mob import *
from music import *
from menu import *
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
Tanya.config_reading('config')
Tanya.player_image.convert()
Tanya.player_image.set_colorkey((255, 255, 255))
finished = False
condition = 0

menu_font = pygame.font.Font(None, 60)

#Tanya.music.main_music(condition)
Music.main_music(condition)

def update_fps():
    """Writes current fps on the screen"""
    fps = str(int(clock.get_fps()))
    fps_text = Tanya.labelFont.render(fps, 1, pygame.Color(RED))
    return fps_text


options_start = [Menu("START GAME", ((WINDOW_SIZE[1] - 250) // 2, (WINDOW_SIZE[0]) // 3), World.menu_display, menu_font),
                 Menu("EXIT", ((WINDOW_SIZE[1] - 110) // 2, (WINDOW_SIZE[0]) // 2.3), World.menu_display, menu_font)]
options_continue = [Menu("CONTINUE", ((WINDOW_SIZE[1] - 200) // 2, (WINDOW_SIZE[0]) // 3), World.display, menu_font),
                    Menu("EXIT", ((WINDOW_SIZE[1] - 110) // 2, (WINDOW_SIZE[0]) // 2.3), World.display, menu_font)]

menu = pygame.transform.scale(pygame.image.load("pictures/winter_terraria.jpg").convert(),
                              (WINDOW_SIZE[0], WINDOW_SIZE[1]))
biom = pygame.transform.scale(pygame.image.load("pictures/biom1.png").convert(),
                              (WINDOW_SIZE[0], WINDOW_SIZE[1]))
World.screen.set_alpha(None)

while not finished:
    World.screen.blit(World.display, (0, 0))
    if condition == 0:
        World.display.blit(World.menu_display, (0, 0))
        World.menu_display.blit(menu, (0, 0))
        for option in options_start:
            option.draw()
        text = menu_event(options_start, World.display)
        if text == "START GAME":
            condition = 1
        elif text == "EXIT":
            finished = True
            Tanya.config_writing('config')
            pygame.quit()
            sys.exit()

    if condition == 2:
        for option in options_continue:
            option.draw()
        text = menu_event(options_continue, World.display)
        if text == "CONTINUE":
            condition = 1
        elif text == "EXIT":
            finished = True
            Tanya.config_writing('config')
            pygame.quit()
            sys.exit()

    elif condition == 1:
        World.display.fill(ICE_COLOR)
        World.display.blit(biom, (0, -150))
        Camera.moving_cam(Tanya.player_rect.x, Tanya.player_rect.y)
        # cavern background style
        pygame.draw.rect(World.display, ICE_COLOR, pygame.Rect(int(0 - Camera.scroll_speed[0]),
                                                               int(175 - Camera.scroll_speed[1]), 725, 200))
        Max.handle_mob(World.tile_surface, World.display, Tanya.player_rect.x, Tanya.player_rect.y,
                       Camera.scroll_speed, Tanya.sheld.object_item)
        Camera_mob.moving_cam(Max.mob_rect.x, Max.mob_rect.y)

        World.building(Camera.scroll_speed)

        Tanya.handle_player(World.tile_surface, World.display, Camera.scroll_speed, Max.alive )
        World.display.blit(update_fps(), (300, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            finished = True
            Tanya.config_writing('config')
        if event.type == KEYDOWN:
            Tanya.is_moving_down(event)
            Tanya.choice_item(event)
            Tanya.workshop(event)
            Tanya.drop_items(event)
            if event.key == K_ESCAPE:
                condition = 2

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
                print(Max.alive)
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


    # pygame.display.flip()
    pygame.display.update()
    clock.tick(120)
