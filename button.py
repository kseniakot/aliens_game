import pygame


class Button():

    def __init__(self, ai_game, msg):
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        self.rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.rect.center = self.screen.get_rect().center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.settings.button_font.render(msg, True, self.settings.button_text_color,
                                                          self.settings.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):

        pygame.draw.rect(self.screen, self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
