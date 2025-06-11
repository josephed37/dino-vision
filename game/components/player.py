import pygame
from config import *

class Player:
    """A class to represent the player character."""

    def __init__(self):
        """Initialize the player's attributes."""
        # Create the player's rectangle object.
        # It's positioned so its bottom is on the ground line.
        self.rect = pygame.Rect(
            PLAYER_START_X,
            GROUND_Y - PLAYER_HEIGHT,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )
        self.color = WHITE
        self.y_velocity = 0
    
    def reset(self): # NEW METHOD
        """Reset the player to its starting position and state."""
        self.rect.y = GROUND_Y - PLAYER_HEIGHT
        self.y_velocity = 0
        
    def jump(self): # NEW METHOD
        """Makes the player jump, but only if they are on the ground."""
        # Only jump if the bottom of the rect is at the ground line
        if self.rect.bottom == GROUND_Y:
            self.y_velocity = -JUMP_STRENGTH

    def update(self): # NEW METHOD
        """Update the player's position based on gravity."""
        # Apply gravity
        self.y_velocity += GRAVITY
        # Update position
        self.rect.y += self.y_velocity

        # Prevent falling through the ground
        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.y_velocity = 0

    def draw(self, screen):
        """Draw the player on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)