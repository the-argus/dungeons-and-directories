import arcade
from Engine import GameEngine as Engine
from constants.screen import (  SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE )

def main():
    """ run when this script is executed """
    engine = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    engine.setup()
    
    engine.load("examplescene")

    arcade.run()


if __name__ == "__main__":
    main()
