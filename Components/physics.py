from .base_visible import BaseVisible
from typing import Optional, Union, Tuple
# vv physics component body types vv
# from constants.physics import STATIC, DYNAMIC, KINEMATIC
import arcade
import pymunk

class Physics(BaseVisible):
    def __init__(   self, physics_engine : arcade.PymunkPhysicsEngine = None,
                    mass: float = None,
                    friction: float = None,
                    elasticity: Optional[float] = None,
                    moment_of_inertia: Optional[float] = None,  # correct spelling
                    body_type: int = None,
                    damping: Optional[float] = None,
                    gravity: Union[pymunk.Vec2d, Tuple[float, float]] = None,
                    max_velocity: int = None,
                    max_horizontal_velocity: int = None,
                    max_vertical_velocity: int = None,
                    radius: float = None,
                    collision_type: Optional[str] = None
                ):
        """
        Creates physics object and adds it to an engine.  Read docs for
        arcade.PymunkPhyiscsEngine.add_sprite for more information on
        the parameters of this function.
        """
        super().__init__()
        self.engine = physics_engine

        # take the important arguments and store them for add_sprite later if we get a parent
        self._physics_args_container = locals()
        templist = ["self"]
        for key, value in self._physics_args_container.items():
            if value is None or key[:2] == "__":
                templist.append(key)
        for key in templist:
            self._physics_args_container.pop(key)
    
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        is_as = isinstance(value, arcade.Sprite)

        if is_as or value is None:
            self._parent = value
            if is_as:
                self.engine = value.physics_engine
                self.engine.add_sprite(value, **self._physics_args_container)
        else:
            raise ValueError(f"{self.__class__.__name__} Component can only be assigned to an instance of an arcade sprite.")
    
    def apply_impulse(self, impulse: Tuple[float, float]):
        self.engine.apply_impulse(self.parent, impulse)

    def set_velocity(self, velocity: Tuple[float, float]):
        self.engine.set_velocity(self.parent, velocity)

    def set_position(self, position: Union[pymunk.Vec2d, Tuple[float, float]]):
        self.engine.set_position(self.parent, position)