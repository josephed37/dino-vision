import pygame
import random
from config import *

class Obstacle:
    """A class to represent a single obstacle sprite."""

    def __init__(self):
        """Initialize the obstacle's attributes by randomly choosing an image."""
        image_files = ['Cactus (1).png', 'Cactus (3).png', 'Crate.png']
        chosen_image_file = random.choice(image_files)
        image_path = f'assets/sprites/obstacle/{chosen_image_file}'
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        self.x_pos = float(SCREEN_WIDTH)
        
        self.rect = self.image.get_rect(
            bottomleft=(self.x_pos, GROUND_Y + PLAYER_FEET_OFFSET)
        )
        self.passed = False

    def update(self, speed, dt):
        """Move the obstacle from right to left based on the current game speed."""
        self.x_pos -= speed * dt
        self.rect.x = round(self.x_pos)

    def draw(self, screen):
        """Draw the obstacle sprite on the screen."""
        screen.blit(self.image, self.rect)