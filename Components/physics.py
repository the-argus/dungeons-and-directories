from .base_visible import BaseVisible
import arcade

class Physics(BaseVisible):
    def __init__(self, physics_engine : arcade.PymunkPhysicsEngine):
        super().__init__()