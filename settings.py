import pygame
import pygame.font


class Settings():

    def __init__(self):
        self.initialize_dynamic_settings()

        # screen settings
        self.background_color = (230, 230, 230)
        self.screen_width = 1200
        self.screen_height = 800

        # ship settings
        self.ship_limit = 3

        # bullet settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_limit = 3

        # alien settings
        self.alien_y_speed = 10
        self.fleet_direction = 1

        # button settings
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 255, 0)
        self.button_text_color = (255, 255, 255)
        self.button_font = pygame.font.SysFont(None, 48)

        # game settings
        self.speed_scale = 1.1
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        self.alien_x_speed = 0.75
        self.bullet_speed = 1.0
        self.ship_speed = 1.5

        # score settings
        self.alien_value = 50
