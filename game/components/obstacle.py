import pygame
from config import *

class Obstacle:
    """A class to represent a single obstacle."""

    def __init__(self):
        """Initialize the obstacle's attributes."""
        # Create the obstacle's rectangle object.
        # It spawns just off the right side of the screen.
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            GROUND_Y - OBSTACLE_HEIGHT,
            OBSTACLE_WIDTH,
            OBSTACLE_HEIGHT
        )
        self.color = RED
        self.speed = OBSTACLE_SPEED

    def update(self):
        """Move the obstacle from right to left."""
        self.rect.x -= self.speed

    def draw(self, screen):
        """Draw the obstacle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)