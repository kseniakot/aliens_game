import pygame


class Settings():

    def __init__(self):
        # screen settings
        self.background_color = (230, 230, 230)
        self.screen_width = 1200
        self.screen_height = 800

        # ship settings
        self.ship_speed = 1.5

        # bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_limit = 3

        # alien settings
        self.alien_x_speed = 0.75
        self.alien_y_speed = 10
        self.fleet_direction = 1
