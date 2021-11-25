import arcade
from .base import Base

class BaseVisible(Base):
    def __init__(self):
        super().__init__()

    """the property below ensures that this component can only be added to an arcade sprite (gameobjectvisible)"""
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        if isinstance(value, arcade.Sprite) or value is None:
            self._parent = value
        else:
            raise ValueError(f"{self.__class__.__name__} Component can only be assigned to an instance of an arcade sprite.")