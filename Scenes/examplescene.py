import pymunk
from constants.screen import SCREEN_HEIGHT, SCREEN_WIDTH
from Engine import Scene
from GameObjects import Camera, Player

def examplescene():
    scene = Scene()

    # add objects
    scene.add_object(Camera)
    scene.add_object(Player)

    # add walls
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
        scene.add_physics_object(body[i], shape[i])
    
    return scene