# constants relating to the player's physics and controls

from constants.physics import MOMENT_INF

SIMPLE_MOVE_SPEED = 200

MASS = 1e-2

MOVE_FORCE = MASS * 1e3

FRICTION = 0.2
INERTIA = MOMENT_INF
# disabled
DAMPING = None
MAX_VELOCITY = None