import pygame
from config import *
import os

def load_animation_frames(folder_path, frame_count):
    """Loads a sequence of animation frames from a folder."""
    frames = []
    for i in range(1, frame_count + 1):
        filename = f'{folder_path} ({i}).png'
        image = pygame.image.load(filename).convert_alpha()
        scaled_image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        frames.append(scaled_image)
    return frames

class Player:
    """A class to represent the animated player character."""

    def __init__(self):
        """Initialize the player's attributes and load animations."""
        self.animations = {
            'run': load_animation_frames('assets/sprites/dino/run/Run', 8),
            'jump': load_animation_frames('assets/sprites/dino/jump/Jump', 12),
            'dead': load_animation_frames('assets/sprites/dino/dead/Dead', 8)
        }
        
        self.state = 'run'
        self.frame_index = 0
        self.image = self.animations[self.state][int(self.frame_index)]
        
        self.ground_level = GROUND_Y + PLAYER_FEET_OFFSET
        
        self.rect = self.image.get_rect(bottomleft=(PLAYER_START_X, self.ground_level))
        self.y_velocity = 0

    def reset(self):
        """Reset the player to its starting state."""
        self.state = 'run'
        self.rect.bottom = self.ground_level
        self.y_velocity = 0

    def jump(self):
        """Makes the player jump, but only if they are on the ground and not dead."""
        if self.rect.bottom == self.ground_level and self.state != 'dead':
            self.y_velocity = -JUMP_STRENGTH
            self.state = 'jump'
            self.frame_index = 0

    def die(self):
        """Sets the player state to dead."""
        if self.state != 'dead':
            self.state = 'dead'
            self.frame_index = 0

    def update(self, dt):
        """Update the player's state, physics, and animation each frame."""
        if self.state != 'dead':
            self.y_velocity += GRAVITY * dt
            self.rect.y += self.y_velocity * dt

            if self.rect.bottom > self.ground_level:
                self.rect.bottom = self.ground_level
                self.y_velocity = 0
                if self.state != 'run':
                    self.state = 'run'
                    self.frame_index = 0
        
        self.animate(dt)

    def animate(self, dt):
        """Cycle through animation frames."""
        current_animation = self.animations[self.state]
        
        self.frame_index += ANIMATION_SPEED * dt
        
        if self.frame_index >= len(current_animation):
            if self.state == 'run' or self.state == 'jump':
                self.frame_index = 0
            else:
                self.frame_index = len(current_animation) - 1
        
        self.image = current_animation[int(self.frame_index)]

    def draw(self, screen):
        """Draw the player's current animation frame."""
        screen.blit(self.image, self.rect)