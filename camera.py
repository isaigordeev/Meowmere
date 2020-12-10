from game_map import WINDOW_SIZE
class Camera:
    def __init__(self):
        self.scroll_speed = [0, 0]
        self.scroll_mob_speed = [0,0]
    def moving_cam(self, player_x, player_y):
        self.scroll_speed[0] += (player_x - self.scroll_speed[0] - WINDOW_SIZE[0]/2) / 10
        self.scroll_speed[1] += (player_y - self.scroll_speed[1] - (WINDOW_SIZE[1]-100)/2) / 10

    def moving_mob_cam(self, mob_x, mob_y):
        self.scroll_mob_speed[0] += (mob_x - self.scroll_speed[0]) / 10
        self.scroll_mob_speed[1] += (mob_y - self.scroll_speed[1]) / 10




