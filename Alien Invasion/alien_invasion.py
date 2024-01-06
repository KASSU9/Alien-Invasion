import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from rocket import Rocket
from explosion import Explosion
from boss_alien import AlienBoss
from sphere_bullet import SphereBullet


clock = pygame.time.Clock()

"""
Dying on normal doesn't reset the missiles
"""

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    
    def __init__(self):
        """Initialize the game, and create game resources:"""
        pygame.init()
        self.settings = Settings()
        
        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width 
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game statistics,
        #    and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.sphere_bullets = pygame.sprite.Group()
        
        # Create the alien fleet, a star and a boss function instances
        
        self.star = Star(self)
        self._create_boss()
        
        # Make the Play button
        self.play_button = Button(self, "Play", "center")
        
        # Make difficulty buttons
        self.normal_button = Button(self, "Normal", "midleft")
        self.hard_button = Button(self, "Hard", "midright")
        
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            clock.tick(60) # Game FPS
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_rockets()
                if self.stats.level % 5 != 0:
                    self._update_aliens()
                else:
                    self._update_bosses()
                    self._update_sphere_bullets()
                
                self._update_explosions()
                
            
            self._update_screen()
            
            
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.check_high_score()
                with open("high_score.txt", "w") as f:
                    f.write(str(self.stats.high_score))
                sys.exit()
            
            elif event.type == pygame.MOUSEMOTION:
                motion_mouse_pos = pygame.mouse.get_pos()
                self._check_mouse_hover_pos(motion_mouse_pos, self.play_button)
                self._check_mouse_hover_pos(motion_mouse_pos, self.normal_button)
                self._check_mouse_hover_pos(motion_mouse_pos, self.hard_button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_difficulty_buttons(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_elements(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_mouse_hover_pos(self, mouse_pos, button):
        """Change the color of a button if mouse is hovering over it"""
        mouse_over_button = button.rect.collidepoint(mouse_pos)
        # Set a darker color if mouse is hovering over a button
        if mouse_over_button and not self.stats.game_active:
            button.button_color = button.hover_over_color
            button.color_changed = True
        # Reset the color back to normal if mouse is not over a button
        if not mouse_over_button and not self.stats.game_active and button.color_changed:
            button.button_color = button.button_color_perma
            button.color_changed = False
            
            
    def _check_difficulty_buttons(self, mouse_pos):
        """Apply the correct difficulty level"""
        normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        
        if normal_button_clicked and not self.stats.game_active:
            # Set difficulty to normal
            self.settings.bullets_allowed = 8
            self.settings.ship_limit = 2
            self.stats.difficulty_set = True
        elif hard_button_clicked and not self.stats.game_active:
            # Set difficulty to hard
            self.settings.bullets_allowed = 5
            self.settings.ship_limit = 0
            self.stats.difficulty_set = True
            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active and self.stats.difficulty_set:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            self._start_game()
            
    def _start_game(self):
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score() # Reset the score when a new game starts
        self.sb.prep_level() # Ensure that the level counter is correct
        self.sb.prep_ships() # Prep ships according to ships left
        
        # Get rid of any remaining aliens, bullets and rockets
        self.aliens.empty()
        self.bullets.empty()
        self.rockets.empty()
        self.explosions.empty()
        self.sphere_bullets.empty()
        # self.bosses.empty()

        
        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
    
    def _check_keydown_elements(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.sb.check_high_score()
            with open("high_score.txt", "w") as f:
                f.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_f:
            self._fire_rocket()
        elif event.key == pygame.K_p and not self.stats.game_active and \
        self.stats.difficulty_set:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            self._start_game()
            
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _fire_rocket(self):
        """Create a new rocket and add it to the rockets group"""
        if self.settings.rocket_limit >= 1 and self.stats.game_active:
            self.settings.rocket_side *= -1
            self.settings.rocket_limit -= 1
            new_rocket = Rocket(self)
            self.rockets.add(new_rocket)
            self.sb.prep_rockets()
            
    def _fire_sphere_bullet(self):
        """Create a new sphere bullet and add it to their group"""
        screen = self.screen.get_rect()
        small_screen = screen.centery+2*(screen.centery/3)
        for boss in self.bosses.copy():
            if boss.rect.top > small_screen:
                break
            elif boss.rect.bottom > screen.centery:
                self._fire_three_spheres()
            else:
                self._fire_five_spheres()
            
    def _fire_three_spheres(self):
        left_bullet = SphereBullet(self, 1)
        straight_bullet = SphereBullet(self, 3)
        right_bullet = SphereBullet(self, 2)
    
        self.sphere_bullets.add(left_bullet, straight_bullet, right_bullet)
        
    def _fire_five_spheres(self):
        left_bullet = SphereBullet(self, 1)
        straight_bullet = SphereBullet(self, 3)
        right_bullet = SphereBullet(self, 2)
        left_straight_bullet = SphereBullet(self, 4)
        right_straight_bullet = SphereBullet(self, 5)
    
        self.sphere_bullets.add(left_bullet, straight_bullet, right_bullet,
                                left_straight_bullet, right_straight_bullet)       
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
            
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        if self.stats.level % 5 != 0:
            self._check_bullet_alien_collisions()
        else:
            self._check_bullet_boss_collisions()
        
    def _update_rockets(self):
        """Update position of all rockets and get rid of old rockets"""
        # Update bullet positions
        self.rockets.update()
        
        # Get rid of rockets that have disappeared
        for rocket in self.rockets.copy():
            if rocket.rect.bottom <= 0:
                self.rockets.remove(rocket)
        
        if self.stats.level % 5 != 0:
            self._check_rocket_alien_collisions()
        else:
            self._check_rocket_boss_collisions()
            
    def _update_sphere_bullets(self):
        """Update positions of sphere bullets, check for collisions
          and remove old bullets
        """
        self.sphere_bullets.update()
        
        # Get rid of bullets that have disappeared
        for sphere_bullet in self.sphere_bullets.copy():
            if sphere_bullet.rect.top >= self.screen.get_rect().bottom:
                self.sphere_bullets.remove(sphere_bullet)
        
        self._check_sphere_ship_collisions()
                
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, self.settings.bullet_breaks, True)
        
        if collisions: # Count points for aliens shot down
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
        
        if not self.aliens: # Activates if the fleet has been destroyed
            self._start_new_level()
            
    def _check_rocket_alien_collisions(self):
        """Respond to rocket-alien collisions"""
        rocket_collisions = pygame.sprite.groupcollide(
            self.rockets, self.aliens, True, False)
        # Create explosions if rockets hit aliens
        if rocket_collisions:
            for explosion in rocket_collisions.values():
                exp = Explosion(self, list(rocket_collisions.keys())[0].rect.center)
                self.explosions.add(exp)
                
        # Remove aliens that were blown up
        explosion_collisions = pygame.sprite.groupcollide(
            self.explosions, self.aliens, False, True)
        if explosion_collisions: # Count points for aliens blown up
            for aliens in explosion_collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
                
    def _check_bullet_boss_collisions(self):
        """Respond to bullet-boss collisions"""
        # Remove any bullets that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.bosses, True, False)
        
        if collisions: # Damage the boss
            for boss in self.bosses:
                boss.health -= 1 # reduce the health
                if boss.health < 1:
                    self.bosses.empty() # kill the boss
                    self.stats.score += self.settings.boss_points # add score points
                    self.sb.prep_score()
                    
        if not self.bosses: # activates if the boss is dead
            self._start_new_level()
        
                
        
    def _check_rocket_boss_collisions(self):
        """Respond to rocket-boss collisions"""
        # Remove any rockets that have collided
        rocket_collisions = pygame.sprite.groupcollide(
            self.rockets, self.bosses, True, False)
        
        # Create explosions if rockets hit the boss
        if rocket_collisions:
            for explosion in rocket_collisions.values():
                exp = Explosion(self, list(rocket_collisions.keys())[0].rect.center)
                self.explosions.add(exp)
        
        if rocket_collisions: # Damage the boss
            for boss in self.bosses:
                boss.health -= 5 # reduce the health
                if boss.health < 1:
                    self.bosses.empty() # kill the boss
                    self.stats.score += self.settings.boss_points # add score points
                    self.sb.prep_score()
                    
        if not self.bosses: # activates if the boss is dead
            self._start_new_level()
            
    def _check_sphere_ship_collisions(self):
        """Respond to sphere-ship collisions"""
        # check collisions and remove bullets hit
        if pygame.sprite.spritecollideany(self.ship, self.sphere_bullets):
            self._ship_hit()

          
    def _start_new_level(self):
        # Destroy existing bullets and create a new fleet
        self.bullets.empty()
        self.rockets.empty()
        self.explosions.empty()
        self.sphere_bullets.empty()

        if self.stats.level % 5 != 0:
            self._create_fleet()
        else:
            self._create_boss()
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()
        
        # Reset rocket count
        self.settings.rocket_limit = 4
        self.sb.prep_rockets()

                
                
    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # Look for aliens hitting the bottom of the screens
        self._check_aliens_bottom()
        
    def _update_explosions(self):
        """Check if explosions should be on the screen anymore"""
        for explosion in self.explosions.sprites():
            explosion.update()
            
    def _update_bosses(self):
        """Check if the boss is at an edge,
          then bounce it from the edge.
          Make it fire and check for collisions
        """
        # self.bosses._check_top_edge()
        for boss in self.bosses:
            # Check edge collisions
            boss._check_edges()
            if boss.edge: 
                boss.change_direction()
                boss.last_update = pygame.time.get_ticks()
            # Change to a radnom direction if it hasn't been updated in time
            boss.new_direction()
        
            # Fire bullets
            self._boss_firing(boss)
        
        # Move the boss
        self.bosses.update()
        
        # Check for ship-boss collisions
        if pygame.sprite.spritecollideany(self.ship, self.bosses):
            self._ship_hit()
            
    def _boss_firing(self, boss):
        """Fire a sphere bullet pereodically"""
        now = pygame.time.get_ticks()
        if now - boss.last_bullet > boss.bullet_time:
            self._fire_sphere_bullet()
            boss.last_bullet = pygame.time.get_ticks()
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Reset the rocket count to 4 and update scoreboard
            self.settings.rocket_limit = 4
            self.sb.prep_rockets()
            
            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            self.bosses.empty()
            self.sphere_bullets.empty()
            self.rockets.empty()
            
            
            
            # Create a new fleet or boss and center the ship
            if self.stats.level % 5 != 0:
                self._create_fleet()
            else:
                self._create_boss()
            
            self.ship.center_ship()
            
            # Pause
            sleep(0.5)
        else:
            # Reset the rocket count to 4 and update scoreboard
            self.settings.rocket_limit = 4
            self.sb.prep_rockets()

            self.stats.game_active = False
            self.stats.difficulty_set = False
            self.sb.check_high_score()
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        """Chech if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break
        
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one aline width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        

        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = (self.settings.screen_height - (9 * alien_height) - # 8
                              ship_height)

        if self.settings.full_screen:
            available_space_x = self.screen.get_rect().width - (2 * alien_width)
            # the scale must be adjusted for each resolution
            scale_for_res = 10 
            available_space_y = (self.screen.get_rect().height - (scale_for_res * alien_height) - 
                                 ship_height)
        
        # Determine the number of rows of aliens that fit on the screen
        # And the amount of aliens that fit in a row
        number_rows = available_space_y // (2 * alien_height)
        number_aliens_x = available_space_x // (2 * alien_width) # Floor division
        
        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_width * 1.5 + 2.8 * alien_height * row_number # 2.6
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)
        
    def _create_boss(self):
        """Create a boss alien and palce it in the level"""
        screen_rect = self.screen.get_rect()
        boss = AlienBoss(self)
        boss.rect.center = screen_rect.center
        self.bosses.add(boss)
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.star.draw_stars()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for rocket in self.rockets.sprites():
            rocket.blitme()
        
        if self.stats.level % 5 != 0:
            self.aliens.draw(self.screen)
        else:
            self.bosses.draw(self.screen)
            for sphere_bullet in self.sphere_bullets.sprites():
                sphere_bullet.draw_bullet()
        
        for explosion in self.explosions.sprites():
            explosion.blitme()
        
        # Draw the score inforamtion
        self.sb.show_score()
        
        # Draw the buttons if the game is inactive
        if not self.stats.game_active:
            self._draw_button(self.play_button)
            self._draw_button(self.normal_button)
            self._draw_button(self.hard_button)
            
        pygame.display.flip()
            
    def _draw_button(self, button):
        """Draw a button onto the screen"""
        if button.color_changed: # Dark button
            button.draw_button(button.dark_msg_image,
                                         button.dark_msg_image_rect)
        else: # Regular button
            button.draw_button(button.msg_image,
                                         button.msg_image_rect)


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()