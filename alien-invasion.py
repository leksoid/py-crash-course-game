import pygame
import sys
from settings import Settings
from ship import Ship
from alien import Alien
from sys import argv
from bullet import Bullet


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """ Init the game and create game resources"""
        pygame.init()
        self.settings = Settings()
        if len(argv) > 1:
            if argv[1] == 'fullscreen':
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.settings.screen_height = self.screen.get_rect().height
                self.settings.screen_width = self.screen.get_rect().width
            elif argv[1] == 'window':
                self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_aliens_fleet()

        # Set the background color
        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Start the main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Make the recently drawn screen visible
        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and get rid of unused bullets"""
        self.bullets.update()
        self._delete_bullets()
        self._check_collisions_and_create_fleet()

    def _delete_bullets(self):
        # Get rid of bullets that reach top of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_collisions_and_create_fleet(self):
        ## check collisions
        # if any, delete 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, 
                True, True)    
        if not self.aliens:
            self.bullets.empty()
            self._create_aliens_fleet()
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        

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
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_aliens_fleet(self):
        """Create the fleet of aliens"""
        alien = Alien(self)
        # .size returns a tuple (width, height)
        alien_width, alien_height = alien.rect.size 
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # how many rows we need?
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height 
                                - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create first row of aliens
        for row in range(number_rows):
            for each in range(number_aliens_x):
                self._create_alien(each, row)
    
    def _create_alien(self, alien_number, row):
        """Create an alien and place it in a row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.is_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
