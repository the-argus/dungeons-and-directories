from math import atan2, cos, sin
from .base_visible import BaseVisible
from .physics import Physics
from constants.player import SIMPLE_MOVE_SPEED, MOVE_FORCE
from constants.controls import (FORWARD,
                                BACK,
                                LEFT,
                                RIGHT,
                                FULLSCREEN
)

class PlayerControl(BaseVisible):
    def __init__(self):
        super().__init__()

    def control(self, keys, delta_time):
        p = self.parent

        if not p:
            return
        
        yin = keys.control_is_pressed(FORWARD) - keys.control_is_pressed(BACK)
        xin = keys.control_is_pressed(RIGHT) - keys.control_is_pressed(LEFT)
        theta = atan2(yin, xin)

        # do simple collision-less movement if there is no physics component
        if not p.Component(Physics):
            p.center_x += SIMPLE_MOVE_SPEED * xin * abs(cos(theta)) * delta_time
            p.center_y += SIMPLE_MOVE_SPEED * yin * abs(sin(theta)) * delta_time
        else:
            # actual physics using arcade pymunk physics engine
            xi = ( MOVE_FORCE * xin * abs(cos(theta)) * delta_time )
            yi = ( MOVE_FORCE * yin * abs(sin(theta)) * delta_time )
            p.apply_impulse((xi, yi))