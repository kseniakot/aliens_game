import pygame


class Statistics():

    def __init__(self, ai_game):
        self.high_score = 0
        self.settings = ai_game.settings
        self.reset_stat()
        self.game_active = False

    def reset_stat(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
