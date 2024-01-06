class Settings:
    """A class to store all settings for Alien Invasion"""
    
    def __init__(self):
        #Initialize the game's static settings
        
        # Screen settings
        # The game is recommended to be played in 1920x1080p
        # Other resoltutions require chaning a variable in _create_fleet and adjusting the ui
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0) # 230
        self.full_screen = False
        
        # Ship settings 
        self.ship_limit = 2
        
        # Bullet settings
        self.bullet_width = 3 # 3 
        self.bullet_height = 13
        self.bullet_color = (0, 255, 0)
        self.bullets_allowed = 8
        self.bullet_breaks = True
        
        # Sphere bullet settings
        self.sphere_bullet_color = (0, 0, 255)
        self.sphere_bullet_height = 25
        self.sphere_bullet_width = 25
        self.sphere_bullet_radius = 20
        
        # Alien settings
        self.fleet_drop_speed = 10
        
        # Boss settings
        self.boss_health = 50
        self.boss_bullet_speed = 5
        
        # How quickly the game speeds up
        self.speedup_scale = 1.2
        
        # How quickly the alien points value increase
        self.score_scale = 1.25
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 7
        self.bullet_speed = 6
        self.alien_speed = 2.0 # 2.0
        self.boss_alien_speed = 2.0
        self.rocket_speed = 7

        # fleet_direction of 1 represents right; -1 reprsents left
        self.fleet_direction = 1
        
        # Rocket
        # 1 = left; -1 = right
        self.rocket_side = 1
        self.rocket_limit = 4 
        
        # Scoring
        self.alien_points = 25
        self.boss_points = 600
        
        
    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.boss_alien_speed *= self.speedup_scale
        self.rocket_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        self.boss_points = int(self.boss_points * self.score_scale)