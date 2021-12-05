from .base import Base
from constants.controls import FULLSCREEN
from constants.screen import SCREEN_WIDTH, SCREEN_HEIGHT
from Engine.decorators import on_control_pressed

class Fullscreen(Base):
    def __init__(self, arcade_game_window):
        super().__init__()
        self.arcade_game_window = arcade_game_window

    @on_control_pressed(FULLSCREEN)
    def toggle_fullscreen(self, control, key_manager):
        self.arcade_game_window.set_fullscreen(not self.arcade_game_window.fullscreen)

        # modify viewport to match fullscreen resolution to prevent stretching
        # causes new things to become visible.  I guess you could see outside the map
        # if the game is set to 16:9 but you have a 4:3 monitor
        width, height = self.arcade_game_window.get_size()
        if self.arcade_game_window.fullscreen:
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
        self.arcade_game_window.set_viewport(x1, x2, y1, y2)