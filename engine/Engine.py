from ctypes import ArgumentError
from numbers import Number
from tools import get_unique_id, IDDict
from components.image_rendering import BatchHandler
from CONSTANTS import Components


class GameObject():
    def __init__(self, coords, used_ids):
        self.id = get_unique_id(used_ids)
        self._coords = [coords[0], coords[1]]
        self._y = coords[1]
        self._x = coords[0]
        self.x = coords[0]
        self.y = coords[1]
        self.coords = [self.x, self.y]
    
    @property
    def coords(self):
        return self._coords
    
    @coords.setter
    def coords(self, coords):
        if ((isinstance(coords, tuple) or isinstance(coords, list)
            ) and len(coords) == 2) and isinstance(coords[0], Number) and isinstance(coords[1], Number):
            self._coords = coords
            if coords[0] == self.x and coords[1] == self.y:
                return
            self.x = coords[0]
            self.y = coords[1]
        else:
            raise ArgumentError("Coords must be a two item iterable of numbers.")
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        if value == self.coords[0]:
            return
        self.coords = [value, self.coords[1]]
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if value == self.coords[1]:
            return
        self.coords = [self.coords[0], value]

class Engine():
    """
    Holds dictionaries of all game object data, and contains component managers.
    """
    def __init__(self):
        # master list of all dicts that use object ID as key
        self.references = []

        # objects key'd by ID (useful as a list of used IDs)
        self.objects = IDDict(self)

        # handler for drawing sprites
        self.sprite_list = BatchHandler(self)

        # dict of all component creation methods (key is from the Components enum)
        self._create_component = {
            Components.sprite_renderer : self.sprite_list.add_sprite
        }

    def create_object(self, coords = ()) -> str:
        """Add new object to objects dict and return it."""
        object = GameObject(coords, self.objects)
        self.objects[object.id] = object

        return object
    
    def destroy_object(self, id):
        """Dereference the object and its ID"""
        for dictionary in self.references:
            dictionary.pop(id)

    def add_component(self, object, component_type, **kwargs):
        """
        Add a component of a given type to an object of a given ID.
        Component-specific arguments should be passed through as
        keyword arguments.
        """
        create_component = self._create_component[component_type]
        create_component(object, **kwargs)
    
    def draw(self):
        self.sprite_list.draw()
        
    