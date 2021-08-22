import arcade
import math
from .core import PhysicsObject, Hitbox
from CONSTANTS import (
                    DEFAULT_SIDE,
                    PLAYER_SIZE,
                    PLAYER_MOVE_FORCE,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    AA_RECT,
                    CIRCLE
)


class Player(PhysicsObject):
    """ Player Class """

    def __init__(self, **kwargs):
        super().__init__(
                        engine=kwargs.get('engine'),
                        layers=kwargs.get('layers'),
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
                        engine=kwargs.get('engine'),
                        layers=kwargs.get('layers'),
                        static=True,
                        x=kwargs.get('x'),
                        y=kwargs.get('y'),
                        has_collisions=True,
                        hitbox=Hitbox(self, AA_RECT)
        )
        self.color = arcade.color.RED

    def draw(self):
        arcade.draw_rectangle_filled(
            self.x, self.y, DEFAULT_SIDE, DEFAULT_SIDE, self.color)


class Circle(PhysicsObject):

    def __init__(self, **kwargs):
        super().__init__(
                        engine=kwargs.get('engine'),
                        layers=kwargs.get('layers'),
                        static=True,
                        x=kwargs.get('x'),
                        y=kwargs.get('y'),
                        has_collisions=True,
                        hitbox=Hitbox(self, CIRCLE, radius=100)
        )

    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.hitbox.radius, arcade.color.RED)


class Ball(PhysicsObject):
    def __init__(self, **kwargs):
        super().__init__(
                        engine=kwargs.get('engine'),
                        layers=kwargs.get('layers'),
                        static=False,
                        x=kwargs.get('x'),
                        y=kwargs.get('y'),
                        has_collisions=False,
                        hitbox=Hitbox(self, CIRCLE, radius=15)
        )

    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.hitbox.radius, arcade.color.GREEN)
