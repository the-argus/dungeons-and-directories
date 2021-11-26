from .base import GameObjectVisible
import Components as C
from constants.screen import SCREEN_HEIGHT, SCREEN_WIDTH
from constants.player import MASS, FRICTION, INERTIA, DAMPING, MAX_VELOCITY

def Player(physics_engine):
    """ main character, should only be instantiated once. """
    start_x = SCREEN_WIDTH/2
    start_y = SCREEN_HEIGHT/2
    sprite = "./resources/square.png"
    p = GameObjectVisible(filename=sprite, center_x=start_x, center_y=start_y)

    p.add_component(C.PlayerControl())
    p.add_component(C.Physics(  physics_engine,
                                mass=MASS,
                                friction=FRICTION,
                                moment_of_inertia=INERTIA,
                                damping=DAMPING,
                                max_velocity=MAX_VELOCITY
                            ))

    return p