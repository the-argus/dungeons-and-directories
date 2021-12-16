from .base import Base
from .camera_base import CameraBase
from constants.controls import FULLSCREEN
from constants.screen import SCREEN_WIDTH, SCREEN_HEIGHT
from Engine.decorators import on_control_pressed

class Fullscreen(Base):
    def __init__(self):
        super().__init__()
    
    def _attached(self):
        """called when parent is set"""
        self.base = self.parent.Component(CameraBase)

        self.set_viewport = self.base.set_viewport
        self.get_viewport = self.base.get_viewport
        self.set_fullscreen = self.base.set_fullscreen
        self.get_size = self.base.get_size

    @on_control_pressed(FULLSCREEN)
    def toggle_fullscreen(self, control, key_manager):
        left, right, top, bottom = self.get_viewport()
        self.set_fullscreen(not self.base.fullscreen)

        if self.base.fullscreen:
            self.set_viewport(left, right, top, bottom)

        # removed fullscreen stretch fix because uh if you play with a 4:3 screen.  why
        """
        # modify viewport to match fullscreen resolution to prevent stretching
        # causes new things to become visible.  I guess you could see outside the map
        # if the game is set to 16:9 but you have a 4:3 monitor
        width, height = self.get_size()
        left, right, top, bottom = self.get_viewport()

        # generic fullscreen calculations
        # not relative to camera position because my brain is small
        if self.base.fullscreen:
            if SCREEN_WIDTH > SCREEN_HEIGHT:
                aspect_ratio = height/width
                x1 = 0
                x2 = SCREEN_WIDTH
                y1 = 0
                y2 = int(SCREEN_WIDTH*aspect_ratio)
            else:
                aspect_ratio = width/height
                x1 = 0
                x2 = int(SCREEN_HEIGHT*aspect_ratio)
                y1 = 0
                y2 = SCREEN_HEIGHT
        else:
            x1 = 0
            x2 = SCREEN_WIDTH
            y1 = 0
            y2 = SCREEN_HEIGHT
    
        self.set_viewport(x1, x2, y1, y2)
        """