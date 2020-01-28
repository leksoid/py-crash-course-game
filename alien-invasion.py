import pygame
import sys
from settings import Settings
from ship import Ship
from sys import argv
from bullet import Bullet

script, mode = argv


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """ Init the game and create game resources"""
        pygame.init()
        self.settings = Settings()
        if mode == 'fullscreen':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_height = self.screen.get_rect().height
            self.settings.screen_width = self.screen.get_rect().width
        elif mode == 'window':
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Set the background color
        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            # Get rid of bullets that reach top of screen
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))
            self._update_screen()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Make the recently drawn screen visible
        pygame.display.flip()

    def _check_events(self):
        # Watch for keyboard and mouse events. Quit is the "close" button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_kyedown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_kyedown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """Create a new bullet and add to a group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
