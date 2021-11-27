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
from Engine.decorators import on_control_pressed

class PlayerControl(BaseVisible):
    def __init__(self):
        super().__init__()

    def control(self, key_manager, delta_time):
        p = self.parent

        if not p:
            return
        
        yin = key_manager.control_is_pressed(FORWARD) - key_manager.control_is_pressed(BACK)
        xin = key_manager.control_is_pressed(RIGHT) - key_manager.control_is_pressed(LEFT)
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

    @on_control_pressed([FORWARD, BACK, LEFT, RIGHT])
    def move_control_pressed(self, control, key_manager):
        print(f"control {control} pressed")