from Engine.decorators import on_update
from .base import Base
from .camera_base import CameraBase
from .lerpclampmove import CameraLerpClampMove

def dummy(*args, **kwargs):
    pass

class CameraFollow(Base):
    def __init__(self, engine, follow_target):
        super().__init__()
        self.follow_target = engine.named_objects[follow_target]
        self.move = dummy
    
    def _attached(self):
        self.move = self.parent.Component(CameraLerpClampMove).move
    
    @on_update
    def follow(self, delta_time):
        self.move(self.follow_target.center_x, self.follow_target.center_y)