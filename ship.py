import pygame


class Ship:
    """To manage a ship"""

    def __init__(self, ai_game):
        """Init the ship and place it based on window screen object"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the image and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Start the ship at the midbottom position of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship"""
        self.screen.blit(self.image, self.rect)
