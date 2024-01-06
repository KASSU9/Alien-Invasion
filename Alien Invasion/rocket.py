import pygame
from pygame.sprite import Sprite

from settings import Settings

class Rocket(Sprite):
    """A class to manage rockets fired from the ship"""
    
    def __init__(self, ai_game):
        # Create a rocket object at the ships current position.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the rocket image and set its rect attribute.
        self.image = pygame.image.load("images/rocket_small.png")
        self.rect = self.image.get_rect()
        
        
        # set the correct position of the rocket
        if self.settings.rocket_side == 1:
            self.rect.midleft = ai_game.ship.rect.midleft
        elif self.settings.rocket_side == -1:
            self.rect.midright = ai_game.ship.rect.midright
        
        
        # Store the rocket's position as a decimal value
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the rocket up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.rocket_speed
        # Update the rect position.
        self.rect.y = self.y
        
    def blitme(self):
        """Draw the rocket at its current location."""
        self.screen.blit(self.image, self.rect)