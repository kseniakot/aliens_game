import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # where we want to place the bullet(starting position)
        self.rect.center = ai_game.ship.rect.center
        # we store its y coordinate to smoothly change its speed
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)

