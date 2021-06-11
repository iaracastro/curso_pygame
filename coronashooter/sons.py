import pygame
from pygame import mixer
pygame.init()

class Sounds():

    def soundtrack(self):
        mixer.music.load('corona_soundtrack.mp3')
        mixer.music.play(-1)
