import pygame
import sys

from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from statistics import Statistics
from button import Button
from scoreboard import Scoreboard


class Game():

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("My alien game")
        self.screen.fill(self.settings.background_color)

        self.statistics = Statistics(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()

            if self.statistics.game_active:
                self.ship.update()
                self._update_bullets()
                self._clear_old_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_event()

    def _check_mouse_event(self):
        mouse_pos = pygame.mouse.get_pos()
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.statistics.game_active:
            self.statistics.reset_stat()
            self.statistics.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_SPACE:
            self._fire_bullets()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.background_color)
        self.ship.blit_me()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.draw_score()
        if not self.statistics.game_active:
            self.play_button.draw_button()
        pygame.display.update()

    def _fire_bullets(self):
        if len(self.bullets) < self.settings.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.statistics.score += self.settings.alien_value * len(aliens)
                self.sb.check_high_score()
        if not len(self.aliens):
            self.bullets.empty()
            self._create_fleet()
            self._increase_game_complexity()

    def _clear_old_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < self.screen_rect.top:
                self.bullets.remove(bullet)

    def _create_fleet(self):

        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = self.settings.screen_height - (3 * alien_height) - self.ship.rect.height
        number_aliens_y = available_space_y // (2 * alien_height)

        for number_row in range(number_aliens_x):
            for number_col in range(number_aliens_y):
                new_alien = Alien(self)

                new_alien.x = alien_width + 2 * alien_width * number_row
                new_alien.y = alien.rect.height + 2 * alien.rect.height * number_col

                new_alien.rect.x = new_alien.x
                new_alien.rect.y = new_alien.y

                self.aliens.add(new_alien)

    def _update_aliens(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        self.aliens.update()
        self._check_ship_alien_collisions()
        self._check_aliens_bottom()

    def _check_ship_alien_collisions(self):

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):

        self.statistics.ships_left -= 1

        if self.statistics.ships_left > 0:
            # pause the game
            sleep(0.5)
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self._create_fleet()

        else:
            self.statistics.game_active = False
            pygame.mouse.set_visible(True)
            self.settings.initialize_dynamic_settings()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def _increase_game_complexity(self):
        self.statistics.level += 1
        self.settings.ship_speed *= self.settings.speed_scale
        self.settings.bullet_speed *= self.settings.speed_scale
        self.settings.alien_x_speed *= self.settings.speed_scale
        self.settings.alien_value = int(self.settings.alien_value * self.settings.score_scale)

    def _change_fleet_direction(self):
        self.settings.fleet_direction *= -1
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_y_speed


def main():
    game = Game()
    game.run_game()


if __name__ == '__main__':
    main()
