import arcade
import math
from .core import PhysicsObject, Hitbox
from CONSTANTS import (
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
        arcade.draw_rectangle_filled(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE, self.color)

    def update(self, keys):
         """ Move the player """
         yin = keys["S"] - keys["W"]
         xin = keys["D"] - keys["A"]

         self.enact_force((xin*PLAYER_MOVE_FORCE, yin*PLAYER_MOVE_FORCE))
