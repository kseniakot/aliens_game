import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class Game():

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("My alien game")
        self.screen.fill(self.settings.background_color)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
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
        pygame.display.update()

    def _fire_bullets(self):
        if len(self.bullets) < self.settings.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _clear_old_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < self.screen_rect.top:
                self.bullets.remove(bullet)

    def _update_bullets(self):
        self.bullets.update()
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not len(self.aliens):
            self._create_fleet()

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

    def _change_fleet_direction(self):
        self.settings.fleet_direction *= -1
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_y_speed


def main():
    game = Game()
    game.run_game()


if __name__ == '__main__':
    main()
