from .base import Base
from .camera_base import CameraBase
from utils import lerp, clamp

class CameraLerpClampMove(Base):
    def __init__(self, lerpspeed, x_clamp, y_clamp):
        super().__init__()

        self.x_clamp = x_clamp
        self.y_clamp = y_clamp
        self.lerpspeed = lerpspeed
    
    def _attached(self):
        base = self.parent.Component(CameraBase)
        self.set_viewport = base.set_viewport
        self.get_size = base.get_size
        self.get_viewport = base.get_viewport
    
    def move(self, focus_x, focus_y):
        """Lerp position in approach of target"""
        top, bottom, left, right = self.get_viewport()
        width, height = self.get_size()

        cx = left+(width/2)
        cy = bottom+(height/2)

        # lerp
        new_cx = lerp(cx, focus_x, self.lerpspeed)
        new_cy = lerp(cy, focus_y, self.lerpspeed)

        # clamp
        new_cx = clamp(new_cx, self.x_clamp)
        new_cy = clamp(new_cy, self.y_clamp)

        left = new_cx - (width/2)
        right = new_cx + (width/2)
        bottom = new_cy - (height/2)
        top = new_cy + (height/2)

        self.set_viewport(left, right, bottom, top)