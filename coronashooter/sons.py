import pygame
import os

class Sons():
    def __init__(self):
        from pygame import mixer
        self.path = os.path.join()
        self.load = mixer.music.load()
        self.volume = mixer.music.set_volume()
        self.tocar_som = pygame.music.mixer.Sound()
        self.tocar_music = pygame.music.play()

    def tocar_soundtrack(self, nome):
        nome = self.path('sons', nome)
        self.load(nome)
        self.volume(0.07)
        self.tocar_music(-1)

    #def tocar_som(self):

    def corona_soundtrack(self, soundtrack="corona_soundtrack.mp3"):
        soundtrack = self.path('sons', soundtrack)
        self.load(soundtrack)
        self.volume(0.07)
        self.tocar_music(-1)

    def game_over_sound(self, game_over="game_over.wav"):
        game_over = self.path('sons', game_over)
        self.tocar_som(game_over)
        game_over.play()

    def menu_soundtrack(self, menu_soundtrack="menu_soundtrack.mp3"):
        menu_soundtrack = os.path.join('sons', menu_soundtrack)
        self.load(menu_soundtrack)
        self.volume(0.07)
        self.tocar_music(-1)