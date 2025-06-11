import pygame
import sys
import random
from config import *
from game.components.player import Player
from game.components.obstacle import Obstacle
from game.components.background import Background
from game.components.ground import Ground

def check_collisions(player, obstacles):
    """Check for collisions between the player and any obstacles using smaller hitboxes."""
    player_hitbox = player.rect.inflate(-PLAYER_HITBOX_SHRINK_X, -PLAYER_HITBOX_SHRINK_Y)
    
    for obstacle in obstacles:
        obstacle_hitbox = obstacle.rect.inflate(-OBSTACLE_HITBOX_SHRINK_X, -OBSTACLE_HITBOX_SHRINK_Y)
        
        if player_hitbox.colliderect(obstacle_hitbox):
            player.die()
            return False # Collision detected
    return True # No collisions

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Vision")
clock = pygame.time.Clock()

background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
ground = Ground()
player = Player()

# Game State
game_active = True
game_font = pygame.font.Font(None, 50)

# --- Dynamic Game Variables ---
obstacles = []
current_speed = INITIAL_OBSTACLE_SPEED

# Manual spawn timer variables
obstacle_spawn_timer = pygame.time.get_ticks()
obstacle_spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)

# --- Main Game Loop ---
while True:
    # --- Delta Time Calculation ---
    dt = min(clock.tick(FPS) / 1000.0, 0.1)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                obstacles.clear()
                player.reset()
                current_speed = INITIAL_OBSTACLE_SPEED
                obstacle_spawn_timer = pygame.time.get_ticks()

    # 2. Game Logic
    if game_active:
        background.update(current_speed, dt)
        ground.update(current_speed, dt)
        player.update(dt)
        for obstacle in obstacles:
            obstacle.update(current_speed, dt)
        
        if current_speed < MAX_OBSTACLE_SPEED:
            current_speed += SPEED_ACCELERATION * dt

        current_time = pygame.time.get_ticks()
        if current_time - obstacle_spawn_timer >= obstacle_spawn_interval:
            obstacles.append(Obstacle())
            obstacle_spawn_timer = current_time
            obstacle_spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)

        game_active = check_collisions(player, obstacles)

        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.right > 0]
    
    # 3. Drawing
    screen.fill(BLACK)
    background.draw(screen)
    ground.draw(screen)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
        
    if not game_active:
        game_over_surface = game_font.render('Game Over', True, WHITE)
        restart_surface = game_font.render('Press Space to Restart', True, WHITE)
        game_over_rect = game_over_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
        restart_rect = restart_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(restart_surface, restart_rect)

    # 4. Updating the screen
    pygame.display.flip()

    # 5. Frame Rate Control is now handled by clock.tick() in the dt calculation