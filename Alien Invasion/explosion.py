import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """a class to manage explosions"""
    
    def __init__(self, ai_game, center):
        super().__init__()
        self.screen = ai_game.screen
        
        # Load the explosion image
        self.image = pygame.image.load("images/pow2.png")
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200 # How many milliseconds the explosion will be visible for
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.kill()
            
    def blitme(self):
        """Draw the explosion onto the screen"""
        self.screen.blit(self.image, self.rect)