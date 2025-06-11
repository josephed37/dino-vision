import pygame
import sys
from config import *
from game.components.player import Player
from game.components.obstacle import Obstacle

def check_collisions(player, obstacles):
    """Check for collisions between the player and any obstacles."""
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            return False # Collision detected
    return True # No collisions

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Vision")
clock = pygame.time.Clock()
player = Player()

# Obstacle management
obstacles = []
OBSTACLE_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_SPAWN_EVENT, OBSTACLE_SPAWN_RATE)

# Game State
game_active = True

# NEW: Font initialization
game_font = pygame.font.Font(None, 50) # Use Pygame's default font, size 50


# --- Main Game Loop ---
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
              # Handle input during the active game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == OBSTACLE_SPAWN_EVENT:
                obstacles.append(Obstacle())
        else: # Handle input during the game over state
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset the game
                game_active = True
                obstacles.clear()
                player.reset()

    # 2. Game Logic
    if game_active:
        player.update()
        for obstacle in obstacles:
            obstacle.update()

        game_active = check_collisions(player, obstacles)

        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.right > 0]


    # 3. Drawing
    screen.fill(BLACK)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
        
    # Draw Game Over screen if not active
    if not game_active:
        # Create the text surfaces
        game_over_surface = game_font.render('Game Over', True, WHITE)
        restart_surface = game_font.render('Press Space to Restart', True, WHITE)
        
        # Get the rectangles for positioning
        game_over_rect = game_over_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
        restart_rect = restart_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))

        # Draw the text to the screen
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(restart_surface, restart_rect)


    # 4. Updating the screen
    pygame.display.update()

    # 5. Frame Rate Control
    clock.tick(FPS)