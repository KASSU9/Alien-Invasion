import pygame
from random import randrange
from pygame.sprite import Sprite

class AlienBoss(Sprite):
    """A class to represent a single boss alien"""
    
    def __init__(self, ai_game):
        """Initalize the boss alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        
        
        # load the alien boss image and set its rect attribute
        self.image = pygame.image.load("images/REDUFO2.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        # Start the boss in the middle of the screen
        self.rect.center = self.screen_rect.center
        
        # Store the alien's exact horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Store and edge if boss has hit it
        self.edge = ""
        
        # Store the boss' direction
        self.direction = randrange(0, 4)
        
        # Boss' health
        self.health = self.settings.boss_health
        
        # Time for tracking direction changing
        self.last_update = pygame.time.get_ticks()
        # How many milliseconds between changing direction
        self.time = 1500
        
        # Time for tracking time for shooting
        self.last_bullet = pygame.time.get_ticks()
        # How many milliseconds between shots
        self.bullet_time = 2500
        
    def _check_edges(self):
        """Return and edge if alien boss hits it"""
        self.edge = ""
        
        self._check_right_edge()
        self._check_left_edge()
        self._check_top_edge()
        self._check_bottom_edge()
    
    
    # Functions for checking if the boss is at an edge of the screen
    def _check_right_edge(self):
        if self.rect.right >= self.screen_rect.right:
            self.edge = "right"
    
    def _check_left_edge(self):
        if self.rect.left <= 0:
            self.edge = "left"
        
    def _check_top_edge(self):
        if self.rect.top <= 0:
            self.edge = "top"
        
    def _check_bottom_edge(self):
        if self.rect.bottom >= self.screen_rect.bottom:
            self.edge = "bottom"
        
    def new_direction(self):
        """
        Check the time and select a new
        random direction for the boss accordingly
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.time:
            self.direction = randrange(0, 4)
            self.last_update = pygame.time.get_ticks()
        
    def update(self):
        """Move the alien to a specific direction"""
        if self.direction == 0:
            self._move_upright()
        elif self.direction == 1:
            self._move_downright()
        elif self.direction == 2:
            self._move_downleft()
        elif self.direction == 3:
            self._move_upleft()
        
        
    def _move_upright(self):
        self.x += self.settings.boss_alien_speed
        self.y -= self.settings.boss_alien_speed
        self.rect.x = self.x
        self.rect.y = self.y
        
    def _move_downright(self):
        self.x += self.settings.boss_alien_speed
        self.y += self.settings.boss_alien_speed
        self.rect.x = self.x
        self.rect.y = self.y
        
    def _move_downleft(self):
        self.x -= self.settings.boss_alien_speed
        self.y += self.settings.boss_alien_speed
        self.rect.x = self.x
        self.rect.y = self.y
        
    def _move_upleft(self):
        self.x -= self.settings.boss_alien_speed
        self.y -= self.settings.boss_alien_speed
        self.rect.x = self.x
        self.rect.y = self.y
        
    def change_direction(self):
        """Change the direction of the boss if it has hit an edge"""
        if self.direction == 0:
            if self.edge == "right":
                self.direction = 3
            elif self.edge == "top":
                self.direction = 1
                
        elif self.direction == 1:
            if self.edge == "right":
                self.direction = 2
            elif self.edge == "bottom":
                self.direction = 0
                
        elif self.direction == 2:
            if self.edge == "left":
                self.direction = 1
            elif self.edge == "bottom":
                self.direction = 3
                
        elif self.direction == 3:
            if self.edge == "left":
                self.direction = 0
            elif self.edge == "top":
                self.direction = 2


    def blitme(self):
        """Draw the boss at its current location."""
        self.screen.blit(self.image, self.rect)
        