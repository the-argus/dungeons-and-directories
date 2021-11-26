from .base_visible import BaseVisible
from math import atan2, sin, cos

class ConstantFriction(BaseVisible):
    def __init__(self, friction):
        super().__init__()
        self.friction = friction
    
    def apply_friction():
        p = self.parent
        xv, yv = p.velocity
        p.apply_impulse()

    
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        is_as = isinstance(value, arcade.Sprite)
        has_phys = value.Component(Physics) is not None

        if ( is_as and has_phys ) or value is None:
            self._parent = value
            if value is not None:
                self.engine.add_sprite(value, **self._physics_args_container)
        else:
            raise ValueError(   f"{self.__class__.__name__} Component can only be " +
                                f"assigned to an instance of an arcade sprite with" +
                                f" a {Physics.__name__} Component installed." )
