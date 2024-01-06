import pygame
from pygame.sprite import Sprite

class SphereBullet(Sprite):
    """A class to manage bullets fired from the boss alien"""
    
    def __init__(self, ai_game, direction):
        # Create a bullet object at the boss' current position.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.sphere_bullet_color
        
        # Create a bullet rect at (0, 0) and then set correct position.
        for boss in ai_game.bosses.sprites().copy():
            pos = boss.rect.midbottom
        self.rect = pygame.Rect(0, 0, self.settings.sphere_bullet_width,
            self.settings.sphere_bullet_height)
        self.rect.midbottom = pos
        
        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
        # Direction for bullet movement in numbers
        # 1 Straigth
        # 2
        
        self.direction = direction
        
    def update(self):
        """Move the bullet on the screen."""
        # Update the decimal position of the bullet.
        if self.direction == 1:
            self._move_left()
        elif self.direction == 2:
            self._move_right()
        elif self.direction == 3:
            self._move_straight()
        elif self.direction == 4:
            self._move_left_straight()
        elif self.direction == 5:
            self._move_right_straight()
            
            
    def _move_straight(self):
        """Move the sphere straight down"""
        self.y += self.settings.boss_bullet_speed
        # Update the rect position
        self.rect.y = self.y
        
    def _move_left(self):
        """Move the sphere left and down"""
        self.y += self.settings.boss_bullet_speed
        self.x -= self.settings.boss_bullet_speed
        
        self.rect.y = self.y
        self.rect.x = self.x
        
    def _move_right(self):
        """Move the sphere right and down"""
        self.y += self.settings.boss_bullet_speed
        self.x += self.settings.boss_bullet_speed
        
        self.rect.y = self.y
        self.rect.x = self.x
        
    def _move_left_straight(self):
        """Move the sphere a bit left and down"""
        self.y += self.settings.boss_bullet_speed
        self.x -= self.settings.boss_bullet_speed/2
        
        self.rect.y = self.y
        self.rect.x = self.x
        
    def _move_right_straight(self):
        """Move the sphere a bit left and down"""
        self.y += self.settings.boss_bullet_speed
        self.x += self.settings.boss_bullet_speed/2
        
        self.rect.y = self.y
        self.rect.x = self.x
        
    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.circle(self.screen, self.color, self.rect.center,
                           self.settings.sphere_bullet_radius)