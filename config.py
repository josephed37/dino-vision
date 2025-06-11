# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Frame rate
FPS = 60

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player properties
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 75
PLAYER_FEET_OFFSET = 10 
PLAYER_START_X = 100
GROUND_Y = 500

# Physics properties (VALUES SCALED UP FOR DELTA TIME)
# These are now in "pixels per second"
GRAVITY = 2000
JUMP_STRENGTH = 800

# Animation properties (now in "frames per second")
ANIMATION_SPEED = 12

# Obstacle properties (VALUES SCALED UP FOR DELTA TIME)
OBSTACLE_WIDTH = 45  
OBSTACLE_HEIGHT = 90
INITIAL_OBSTACLE_SPEED = 300  # e.g., 300 pixels per second
MAX_OBSTACLE_SPEED = 800
SPEED_ACCELERATION = 10       # e.g., add 10px/sec to speed every second

MIN_SPAWN_INTERVAL = 900
MAX_SPAWN_INTERVAL = 2000

# Hitbox adjustments (how much to shrink the rect by, in pixels)
PLAYER_HITBOX_SHRINK_X = 25 # Shrink by 25px on left/right
PLAYER_HITBOX_SHRINK_Y = 20 # Shrink by 20px on top/bottom

OBSTACLE_HITBOX_SHRINK_X = 15
OBSTACLE_HITBOX_SHRINK_Y = 10