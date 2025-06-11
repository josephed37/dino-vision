# This is the main entry point for our game.
# This is the main entry point for our game.
import pygame
import sys

# Import the configuration constants
from config import *
from game.components.player import Player
from game.components.obstacle import Obstacle

# --- Initialization ---
# Initialize all imported pygame modules
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Vision")

# Set up the clock for a consistent frame rate
clock = pygame.time.Clock()

#Create an instance of the Player
player = Player()

# Obstacle management
obstacles = []
OBSTACLE_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_SPAWN_EVENT, OBSTACLE_SPAWN_RATE)


# --- Main Game Loop ---
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Handle player input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                
        # Handle obstacle spawning
        if event.type == OBSTACLE_SPAWN_EVENT:
            obstacles.append(Obstacle())
                
    # Game Logic
    player.update()
    
    # Update obstacles
    for obstacle in obstacles:
        obstacle.update()

    # Cleanup off-screen obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle.rect.right > 0]

    
    # 2. Drawing
    # Fill the background with black
    screen.fill(BLACK)
    player.draw(screen)
    
    for obstacle in obstacles:
        obstacle.draw(screen)


    # 3. Updating the screen
    # Update the full display Surface to the screen
    pygame.display.update()

    # 4. Frame Rate Control
    # Ensure the game does not run faster than FPS frames per second
    clock.tick(FPS)