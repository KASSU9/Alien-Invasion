import pygame.font

class Button:
    """Make a button with text and render it on the screen"""
    def __init__(self, ai_game, msg, pos):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.button_color_perma = (0, 255, 0)
        self.hover_over_color = (0, 150, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.color_changed = False
        
        # Build the button's rect object and position it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if pos == "center":
            self.rect.center = self.screen_rect.center
        
        elif pos == "midleft":
            self.rect.center = ((self.screen.get_rect().width/2-300),
                                (self.screen.get_rect().height/2))
        elif pos == "midright":
            self.rect.center = ((self.screen.get_rect().width/2+300),
                                (self.screen.get_rect().height/2))
        
        # The button message needs to be prepped only once
        self._prep_msg(msg)
        self._prep_msg_mouse_over(msg)
        
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and cetner text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def _prep_msg_mouse_over(self, msg):
        """Turn msg into a rendered image with dark background"""
        self.dark_msg_image = self.font.render(msg, True, self.text_color,
                                          self.hover_over_color)
        self.dark_msg_image_rect = self.msg_image.get_rect()
        self.dark_msg_image_rect.center = self.rect.center    
        
    def draw_button(self, image, rect):
        # Draw blank button and the draw a message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(image, rect)