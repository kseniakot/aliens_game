import pygame.font

from pygame.sprite import Group
from ship import Ship


class Scoreboard():

    def __init__(self, ai_game):
        self.ai_game = ai_game

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.statistics = ai_game.statistics

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # Turn score into a rendered image
        rounded_score = round(self.statistics.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.background_color)

        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def prep_high_score(self):
        rounded_score = round(self.statistics.high_score, -1)
        score_str = "{:,}".format(rounded_score)
        self.high_score_image = self.font.render(score_str, True, self.text_color,
                                                 self.settings.background_color)
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.top = self.screen_rect.top
        self.high_score_image_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        level_str = str(self.statistics.level)
        self.level_image = self.font.render(level_str, True, self.text_color,
                                            self.settings.background_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.screen_rect.right - 20
        self.level_image_rect.top = self.score_image_rect.bottom + 15

    def prep_ships(self):
        self.ships = Group()

        for ship_number in range(self.statistics.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def draw_score(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        if self.statistics.high_score < self.statistics.score:
            self.statistics.high_score = self.statistics.score
