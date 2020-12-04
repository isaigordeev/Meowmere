from game_map import *
from player import *

clock = pygame.time.Clock()
pygame.init()


Tanya = Player()

while True:
    screen.fill(BACKGROUND_COLOR)

    screen.blit(Tanya.player_image, Tanya.player_location)

    Tanya.gravitation()

    Tanya.moving()

    Tanya.player_rect.x = Tanya.player_location[0]
    Tanya.player_rect.y = Tanya.player_location[1]

    # if Tanya.player_rect.colliderect(Tanya.test_rect):
    #     pygame.draw.rect(screen, RED, Tanya.test_rect)
    # else:
    #     pygame.draw.rect(screen, BLACK, Tanya.test_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            Tanya.is_moving_up(event)
        if event.type == KEYUP:
            Tanya.is_moving_down(event)
    pygame.display.update()
    clock.tick(60)