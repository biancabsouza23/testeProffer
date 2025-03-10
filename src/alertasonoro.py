import pygame

class AlertaSonoro:
    @staticmethod
    def alerta():
        pygame.mixer.init()
        pygame.mixer.music.load("data/som.mp3")
        pygame.mixer.music.play()