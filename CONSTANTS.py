SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
SCREEN_TITLE = "Dungeons and Directories"
FRAMERATE = 1/60

PLAYER_SIZE = 10
PLAYER_MOVE_FORCE = 100
PLAYER_START = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]

# physics objects default properties
DEFAULT_MASS = 5
DEFAULT_SIDE = 10
DRAG = 0.9/FRAMERATE

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

# layers, used to prevent objects from colliding with one another
LAYERS = {
        "PLAYER": 1,
        "WALLS": 2,
        "TESTING": 3
}
