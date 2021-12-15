import arcade
import pymunk
from Engine import GameEngine as Engine
from constants.screen import (  SCREEN_WIDTH,
                                SCREEN_HEIGHT,
                                SCREEN_TITLE
)
from GameObjects import Player, Camera

def main():
    """ run when this script is executed """
    engine = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    engine.setup()
    
    # init camera
    Camera(engine)

    # add some walls
    temp_room_setup(engine.physics_engine)

    # add floor textures
    temp_floor_textures(engine)

    # spawn the player
    Player(engine)

    arcade.run()


    # ian's jank window transparency fix. can be removed in actual releases, sorry lads
    try:
        os.system(f"xprop -name \"{SCREEN_TITLE}\" -format _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY $(printf 0x%x $((0xffffffff)))")
    except Exception:
        pass

def temp_room_setup(physics_engine):
    body = [None for i in range(4)]
    shape = [None for i in range(4)]
    # ljdvnsmflkgefmws lngemfskmgksfdmklm
    body[0] = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape[0] = pymunk.Segment(body[0], (0, 0), (0, SCREEN_HEIGHT), 0.1)
    body[1] = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape[1] = pymunk.Segment(body[1], (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 0.1)
    body[2] = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape[2] = pymunk.Segment(body[2], (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0), 0.1)
    body[3] = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape[3] = pymunk.Segment(body[3], (SCREEN_WIDTH, 0), (0, 0), 0.1)

    for i in range(4):
        shape[i].friction = 0.1
        physics_engine.space.add(body[i], shape[i])

def temp_floor_textures(engine):
    # initialize floor texture and arcade textures
    floor_tex = arcade.load_texture("resources/raw/cobble.png")


if __name__ == "__main__":
    main()
