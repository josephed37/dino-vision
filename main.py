import pygame
import sys
import random
import os
import cv2
import mediapipe as mp
from config import *
from game.components.player import Player
from game.components.obstacle import Obstacle
from game.components.background import Background
from game.components.ground import Ground
from game.components.vision import Vision

# --- High Score Functions ---
def load_high_score():
    """Loads the high score from a file."""
    if os.path.exists('highscore.txt'):
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        except ValueError:
            return 0
    return 0

def save_high_score(score):
    """Saves the high score to a file."""
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

def check_collisions(player, obstacles):
    """Check for collisions between the player and any obstacles using smaller hitboxes."""
    player_hitbox = player.rect.inflate(-PLAYER_HITBOX_SHRINK_X, -PLAYER_HITBOX_SHRINK_Y)
    
    for obstacle in obstacles:
        obstacle_hitbox = obstacle.rect.inflate(-OBSTACLE_HITBOX_SHRINK_X, -OBSTACLE_HITBOX_SHRINK_Y)
        
        if player_hitbox.colliderect(obstacle_hitbox):
            player.die()
            return False
    return True

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Vision - Game")
clock = pygame.time.Clock()

background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
ground = Ground()
player = Player()
vision = Vision()

# Game State
game_active = True
game_font = pygame.font.Font(None, 40)

# --- Dynamic Game Variables ---
obstacles = []
current_speed = INITIAL_OBSTACLE_SPEED
current_score = 0
high_score = load_high_score()
obstacle_spawn_timer = pygame.time.get_ticks()
obstacle_spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)

# Variable to track previous gesture state for one-shot detection
gesture_made_in_last_frame = False

# --- Main Game Loop ---
while True:
    dt = min(clock.tick(FPS) / 1000.0, 0.1)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vision.close()
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                obstacles.clear()
                player.reset()
                current_speed = INITIAL_OBSTACLE_SPEED
                current_score = 0
                obstacle_spawn_timer = pygame.time.get_ticks()

    # --- Vision Processing and Gesture Detection ---
    vision_frame, vision_results = vision.update()
    
    is_jumping_gesture = False
    if vision_results and vision_results.multi_hand_landmarks:
        hand_landmarks = vision_results.multi_hand_landmarks[0]
        
        # --- UPDATED: Two-Finger Gesture Logic ---
        # Get the required landmarks
        index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP]
        
        middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP]
        
        ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_PIP]
        
        pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_PIP]

        # Condition 1: Index and Middle fingers are extended
        index_finger_is_up = index_tip.y < index_pip.y
        middle_finger_is_up = middle_tip.y < middle_pip.y

        # Condition 2: Ring and Pinky fingers are curled
        ring_finger_is_down = ring_tip.y > ring_pip.y
        pinky_is_down = pinky_tip.y > pinky_pip.y
        
        # A jump gesture is only detected if ALL conditions are true
        if index_finger_is_up and middle_finger_is_up and ring_finger_is_down and pinky_is_down:
            is_jumping_gesture = True

    if vision_frame is not None:
        cv2.imshow('Dino Vision - Webcam', vision_frame)
        cv2.waitKey(1)

    # 2. Game Logic
    if game_active:
        if is_jumping_gesture and not gesture_made_in_last_frame:
            player.jump()
            print("JUMP ACTION TRIGGERED! (Two-finger gesture)")

        gesture_made_in_last_frame = is_jumping_gesture
        
        background.update(current_speed, dt)
        ground.update(current_speed, dt)
        player.update(dt)
        for obstacle in obstacles:
            obstacle.update(current_speed, dt)
        
        if current_speed < MAX_OBSTACLE_SPEED:
            current_speed += SPEED_ACCELERATION * dt

        for obstacle in obstacles:
            if not obstacle.passed and obstacle.rect.right < player.rect.left:
                obstacle.passed = True
                current_score += 10

        current_time = pygame.time.get_ticks()
        if current_time - obstacle_spawn_timer >= obstacle_spawn_interval:
            obstacles.append(Obstacle())
            obstacle_spawn_timer = current_time
            obstacle_spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)

        is_still_active = check_collisions(player, obstacles)
        if game_active and not is_still_active:
             if current_score > high_score:
                high_score = current_score
                save_high_score(high_score)
        game_active = is_still_active

        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.right > 0]
    
    # 3. Drawing
    screen.fill(BLACK)
    background.draw(screen)
    ground.draw(screen)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
        
    score_surface = game_font.render(f'Score: {current_score}', True, WHITE)
    score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(score_surface, score_rect)

    high_score_surface = game_font.render(f'High: {high_score}', True, WHITE)
    high_score_rect = high_score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 60))
    screen.blit(high_score_surface, high_score_rect)
        
    if not game_active:
        game_over_surface = game_font.render('Game Over', True, WHITE)
        restart_surface = game_font.render('Press Space to Restart', True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(restart_surface, restart_rect)

    # 4. Updating the Pygame screen
    pygame.display.flip()
