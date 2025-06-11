import pygame
from config import *
import math

class Ground:
    """Manages the scrolling and tiling of the ground."""

    def __init__(self):
        """Initialize and create the tiled ground surface."""
        self.tile = pygame.image.load('assets/sprites/ground/ground_tile.png').convert_alpha()
        self.tile_width = self.tile.get_width()
        
        num_tiles = math.ceil(SCREEN_WIDTH / self.tile_width) + 1

        self.ground_strip = pygame.Surface((self.tile_width * num_tiles, self.tile.get_height()))
        
        for i in range(num_tiles):
            self.ground_strip.blit(self.tile, (i * self.tile_width, 0))

        self.x_pos = [0.0, float(self.ground_strip.get_width())]
        self.y_pos = GROUND_Y

    def update(self, speed, dt):
        """Update the x-position of the ground strips based on current game speed."""
        self.x_pos[0] -= speed * dt
        self.x_pos[1] -= speed * dt

        if self.x_pos[0] <= -self.ground_strip.get_width():
            self.x_pos[0] = self.x_pos[1] + self.ground_strip.get_width()
        
        if self.x_pos[1] <= -self.ground_strip.get_width():
            self.x_pos[1] = self.x_pos[0] + self.ground_strip.get_width()

    def draw(self, screen):
        """Draw both ground strips to the screen, rounding positions for smooth motion."""
        screen.blit(self.ground_strip, (round(self.x_pos[0]), self.y_pos))
        screen.blit(self.ground_strip, (round(self.x_pos[1]), self.y_pos))