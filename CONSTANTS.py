SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dungeons and Directories"

PLAYER_SIZE = 10
PLAYER_MOVE_FORCE = 10

# physics objects default properties
DEFAULT_MASS = 5
DEFAULT_SIDE = 10

# hitbox types
AA_RECT = 1
RECT = 2
CIRCLE = 3
# specifically a convex polygon but that's annoying to type
POLYGON = 4

# materials, used as an argument when creating physics objects
# tuple format is (density, restitution)
MATERIALS = {
            "Stone": (0.6, 0.2),
            "Bouncy Ball": (0.3, 0.8)
            }

DEFAULT_MAT = MATERIALS["Stone"]