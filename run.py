import arcade
import pymunk
from Engine import GameEngine as Engine
from constants.screen import (  SCREEN_WIDTH,
                                SCREEN_HEIGHT,
                                SCREEN_TITLE
)
from GameObjects import Player, Camera
from Scenes import examplescene

def main():
    """ run when this script is executed """
    engine = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    engine.setup()
    
    engine.load(examplescene)

    arcade.run()


if __name__ == "__main__":
    main()
