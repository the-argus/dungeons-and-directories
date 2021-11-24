from .base import GameObjectVisible
import Components as C
from constants.screen import SCREEN_HEIGHT, SCREEN_WIDTH

def Player():
    """ main character, should only be instantiated once. """
    start_x = SCREEN_WIDTH/2
    start_y = SCREEN_HEIGHT/2
    sprite = "./resources/square.png"
    p = GameObjectVisible(filename=sprite, center_x=start_x, center_y=start_y)

    p.add_component(C.PlayerControl())

    return p