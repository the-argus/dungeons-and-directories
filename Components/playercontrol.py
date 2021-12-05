from math import atan2, cos, sin
from .base_visible import BaseVisible
from .physics import Physics
from constants.player import SIMPLE_MOVE_SPEED, MOVE_FORCE, STOPPING_FORCE
from constants.controls import (FORWARD,
                                BACK,
                                LEFT,
                                RIGHT,
                                FULLSCREEN
)
from Engine.decorators import on_control_pressed, on_control_released, on_update

class PlayerControl(BaseVisible):
    def __init__(self):
        self.xin = 0
        self.yin = 0
        super().__init__()

    @on_update
    def control(self, delta_time):
        p = self.parent

        if not p:
            return
        
        yin = self.yin
        xin = self.xin
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

    @on_control_pressed(FORWARD, BACK, LEFT, RIGHT)
    @on_control_released(FORWARD, BACK, LEFT, RIGHT)
    def move_control_updated(self, control, key_manager):
        self.xin = key_manager.control_is_pressed(RIGHT) - key_manager.control_is_pressed(LEFT)
        self.yin = key_manager.control_is_pressed(FORWARD) - key_manager.control_is_pressed(BACK)
    
    @on_control_released(FORWARD, BACK, LEFT, RIGHT)
    def stop(self, control, key_manager):
        """Whenever the player releases a control, apply a force to stop their movement in that direction."""
        p = self.parent
        if not p:
            return
        if not p.Component(Physics):
            return
        
        vx, vy = p.get_velocity()
        """
        for key, modifiers in control.items():
            if (LEFT.get(key) == modifiers and vx < 0) or (RIGHT.get(key) == modifiers and vx > 0):
                p.set_velocity((STOPPING_FORCE*vx, vy))
                return
            elif (BACK.get(key) == modifiers and vy < 0) or (FORWARD.get(key) == modifiers and vy > 0):
                p.set_velocity((vx, STOPPING_FORCE*vy))
                return
        """
        x_disengaged = not key_manager.control_is_pressed(LEFT) and not key_manager.control_is_pressed(RIGHT)
        y_disengaged = not key_manager.control_is_pressed(FORWARD) and not key_manager.control_is_pressed(BACK)

        for key, modifiers in control.items():
            if x_disengaged and (LEFT.get(key) == modifiers or RIGHT.get(key) == modifiers):
                p.set_velocity((STOPPING_FORCE*vx, vy))
                return
            elif y_disengaged and (FORWARD.get(key) == modifiers or BACK.get(key) == modifiers):
                p.set_velocity((vx, STOPPING_FORCE*vy))
                return
