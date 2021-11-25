# constants relating to general physics calculations
import pymunk
# body types
DYNAMIC = pymunk.Body.DYNAMIC
STATIC = pymunk.Body.STATIC
KINEMATIC = pymunk.Body.KINEMATIC

# infinite moment of inertia for preventing rotation
MOMENT_INF = float('inf')

# percentage of force that is maintained anywhere. 1.0 by defaults
GLOBAL_DAMPING = 0.9

# ends up basically being "how sticky are the walls?"
WALL_FRICTION = 0.1