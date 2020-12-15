import pygame


class Music:
    """"Plays music for the game"""
    pygame.init()
    pygame.mixer.init()

    def main_music(self):
        pygame.mixer.music.load('music/grass.wav')
        pygame.mixer.music.play(-1)

    def break_music(self):
        pygame.mixer.music.load('music/break.wav')
        pygame.mixer.music.play(1)
