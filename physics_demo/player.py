import arcade
import math
from .core import PhysicsObject, Hitbox
from CONSTANTS import (
                    DEFAULT_SIDE,
                    PLAYER_SIZE,
                    PLAYER_MOVE_FORCE,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    AA_RECT
)


class Player(PhysicsObject):
    """ Player Class """

    def __init__(self):
        super().__init__(
                        static=False,
                        x=SCREEN_WIDTH/2,
                        y=SCREEN_HEIGHT/2,
                        hitbox=Hitbox(self, AA_RECT)
        )
        self.color = arcade.color.YELLOW

    def draw(self):
        arcade.draw_rectangle_filled(
            self.x, self.y, PLAYER_SIZE, PLAYER_SIZE, self.color)

    def update(self, delta_time, keys):
        """ Move the player """
        yin = keys["W"] - keys["S"]
        xin = keys["D"] - keys["A"]

        self.enact_force((xin*PLAYER_MOVE_FORCE, yin
                          * PLAYER_MOVE_FORCE))


class Wall(PhysicsObject):
    """ Player Class """

    def __init__(self, **kwargs):
        super().__init__(
                        static=True,
                        x=kwargs.get('x', 0),
                        y=kwargs.get('y', 0),
                        has_collisions=True,
                        hitbox=Hitbox(self, AA_RECT)
        )
        self.color = arcade.color.RED

    def draw(self):
        arcade.draw_rectangle_filled(
            self.x, self.y, DEFAULT_SIDE, DEFAULT_SIDE, self.color)
