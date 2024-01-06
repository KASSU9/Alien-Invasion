import pygame
import random

class Star:
    """a class to represent a single star"""
    
    """based on this code: https://gist.github.com/ogilviemt/9b05a89d023054e6279f"""
    
    def __init__(self, ai_game):
        """Iniatlaize initial settings for creaing stars"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.screen_width, self.screen_height = self.screen_rect.size
        
        self.DARKGREY = (100, 100, 100)
        self.LIGHTGREY = (200, 200, 200)
        self.YELLOW = (230, 230, 0)
        
        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []
        
        self.create_stars()
        
    def create_stars(self):
        # Create starting cordinates for stars of three varying sizes

        for slow_stars in range(50):
            star_loc_x = random.randrange(0, self.screen_width)
            star_loc_y = random.randrange(0, self.screen_height)
            self.star_field_slow.append([star_loc_x, star_loc_y])
        
        for medium_stars in range(35):
            star_loc_x = random.randrange(0, self.screen_width)
            star_loc_y = random.randrange(0, self.screen_height)
            self.star_field_medium.append([star_loc_x, star_loc_y])
            
        for fast_stars in range(15):
            star_loc_x = random.randrange(0, self.screen_width)
            star_loc_y = random.randrange(0, self.screen_height)
            self.star_field_fast.append([star_loc_x, star_loc_y])
    
    def draw_stars(self):
        # update the positions of stars
        for star in self.star_field_slow:
            star[1] += 1
            if star[1] > self.screen_height:
                star[0] = random.randrange(0, self.screen_width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.screen, self.DARKGREY, star, 3)
    
        for star in self.star_field_medium:
            star[1] += 4
            if star[1] > self.screen_height:
                star[0] = random.randrange(0, self.screen_width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.screen, self.LIGHTGREY, star, 2)
            
        for star in self.star_field_fast:
            star[1] += 8
            if star[1] > self.screen_height:
                star[0] = random.randrange(0, self.screen_width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.screen, self.YELLOW, star, 1) 