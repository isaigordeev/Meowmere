import pygame


class Music:
    """"Plays music for the game"""
    pygame.init()
    pygame.mixer.init()

    def main_music(self, condition):
        if condition == 1:
            pygame.mixer.music.load('music/Christmas_menu.wav')
            pygame.mixer.music.play(-1)
        if condition == 0:
            pygame.mixer.music.load('music/Christmas.wav')
            pygame.mixer.music.play(-1)
        if condition == 2:
            pygame.mixer.music.load('music/Christmas_pause_menu.wav')
            pygame.mixer.music.play(-1)

    def break_music(self):
        pygame.mixer.music.load('music/break.wav')
        pygame.mixer.music.play(1)
