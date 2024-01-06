import pygame
from pygame.sprite import Sprite

from settings import Settings

class RocketStats(Sprite):
    """A class to manage how many rockets are left"""
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the rocket image and set its rect attribute.
        self.image = pygame.image.load("images/rocket_stats.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        # Store the rocket's position as a decimal value
        self.y = float(self.rect.y)
