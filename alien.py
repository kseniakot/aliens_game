import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # starting position (near the top left of the screen)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.alien_x_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        if self.rect.right > self.screen.get_rect().right or self.x <= 0:
            return True
        return False

