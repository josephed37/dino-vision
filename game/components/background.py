import pygame
from config import *

class Background:
    """Manages the scrolling parallax background."""

    def __init__(self, screen_width, screen_height):
        """Initialize the background layers."""
        self.bg_images = []
        self.bg_x_pos = []
        self.width = screen_width
        self.height = screen_height

        for i in range(1, 6):
            image = pygame.image.load(f'assets/sprites/background/{i}.png').convert_alpha()
            aspect_ratio = image.get_width() / image.get_height()
            new_height = self.height
            new_width = int(new_height * aspect_ratio)
            scaled_image = pygame.transform.scale(image, (new_width, new_height))
            
            self.bg_images.append(scaled_image)
            self.bg_x_pos.append([0.0, float(new_width)])

        self.speed_ratios = [0.1, 0.25, 0.5, 0.75, 1.0]

    def update(self, speed, dt):
        """Update the x-position of each background layer based on the current game speed."""
        for i in range(len(self.bg_images)):
            self.bg_x_pos[i][0] -= self.speed_ratios[i] * speed * dt
            self.bg_x_pos[i][1] -= self.speed_ratios[i] * speed * dt

            if self.bg_x_pos[i][0] <= -self.bg_images[i].get_width():
                self.bg_x_pos[i][0] = self.bg_x_pos[i][1] + self.bg_images[i].get_width()
            
            if self.bg_x_pos[i][1] <= -self.bg_images[i].get_width():
                self.bg_x_pos[i][1] = self.bg_x_pos[i][0] + self.bg_images[i].get_width()

    def draw(self, screen):
        """Draw both copies of all background layers, rounding positions for smooth motion."""
        for i in range(len(self.bg_images)):
            screen.blit(self.bg_images[i], (round(self.bg_x_pos[i][0]), 0))
            screen.blit(self.bg_images[i], (round(self.bg_x_pos[i][1]), 0))