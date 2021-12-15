import arcade
import pymunk
from Engine import GameEngine as Engine
from constants.screen import (  SCREEN_WIDTH,
                                SCREEN_HEIGHT,
                                SCREEN_TITLE
)
from GameObjects import Player, Camera
from Scenes.examplescene import examplescene

def main():
    """ run when this script is executed """
    engine = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    engine.setup()
    
    engine.load(examplescene)

    # add floor textures
    temp_floor_textures(engine)

    arcade.run()

def temp_floor_textures(engine):
    # initialize floor texture and arcade textures
    floor_tex = arcade.load_texture("resources/raw/cobble.png")


if __name__ == "__main__":
    main()
