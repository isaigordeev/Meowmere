import pygame


class Music:
    """"Plays music for the game"""
    def music(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('music/grass.wav')
        pygame.mixer.music.play(-1)
