from .base import Base

class CameraBase(Base):
    """
    Contains information about the viewport which can be accessed by the other camera components
    via parent.Component(CameraBase).set_viewport and etc
    """
    def __init__(self, arcade_game_window):
        super().__init__()
        self.set_viewport = arcade_game_window.set_viewport
        self.set_fullscreen = arcade_game_window.set_fullscreen
        self.get_size = arcade_game_window.get_size
        self.get_viewport = arcade_game_window.get_viewport
        self._arcade_game_window = arcade_game_window
    
    @property
    def fullscreen(self):
        """
        return a value from the private game window.  do this for all literals from the window
        i dont like having a full on reference to the engine stored in a component except when
        absolutely necessary :(
        """
        return self._arcade_game_window.fullscreen