import pyglet
import os
from enum import Enum

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
SCREEN_TITLE = "Dungeons and Directories"
FRAMERATE = 1/60

PLAYER_SIZE = 10
PLAYER_MOVE_FORCE = 100
PLAYER_START = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]

# used by tools
MAX_ID_ITERATIONS = 30

# z value of images in a pyglet batch basically
LAYERS = {
    "background": pyglet.graphics.OrderedGroup(0),
    "midground": pyglet.graphics.OrderedGroup(1),
    "foreground": pyglet.graphics.OrderedGroup(2)
}
DEFAULT_LAYER = LAYERS["background"]

# constant which I think exists somewhere in pyglet but idk so im just hardcoding
# a copy here
DEFAULT_USAGE = 'dynamic'

class Components(Enum):
    sprite_renderer = 0