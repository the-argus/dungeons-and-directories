import math

from tools import arcade_sprite, compass_atan
from engine.physics.object import PhysicsObject
from CONSTANTS import (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    PLAYER_START,
                    PLAYER_MOVE_FORCE
)
"""
this custom class exists because of the extra arg in the on_update function
otherwise this would be better to do with engine.create_object
"""


class Player(PhysicsObject, arcade_sprite):
    def __init__(self, *args, **kwargs):
        arcade_sprite.__init__(self, *args, **kwargs)
        physics_kwargs = kwargs

        physics_kwargs['x'] = PLAYER_START[0]
        physics_kwargs['y'] = PLAYER_START[1]
        physics_kwargs['static'] = False

        PhysicsObject.__init__(self, **physics_kwargs)

    def update(self, delta_time, keys):
        xin = keys["D"] - keys["A"]
        yin = keys["W"] - keys["S"]

        is_moving = xin != 0 or yin != 0

        dir = compass_atan(yin, xin)


        force = (is_moving*PLAYER_MOVE_FORCE*math.cos(dir),
                 is_moving*PLAYER_MOVE_FORCE*math.sin(dir))
        
        force = (xin*PLAYER_MOVE_FORCE, yin*PLAYER_MOVE_FORCE)
        self.enact_force(force)
