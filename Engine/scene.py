

class Scene:
    """
This class stores unregistered physics, game objects, and textures.
It is a container which is meant to be serialized and then later
read from json files.
"""
    def __init__(self):
        # list of functions to create objects
        self.objects = []

        # list of pymunk physics objects to be registered, in (Body, Shape) pairs
        self.physics_objects = []
    
    def add_physics_object(self, body, shape):
        container = (body, shape)
        if container not in self.physics_objects:
            self.physics_objects.append(container)
        else:
            raise ValueError(f"body {body} and shape {shape} are already listed in physics objects.")
    
    def add_object(self, object_creation_func):
        if object_creation_func not in self.objects:
            self.objects.append(object_creation_func)
        else:
            raise ValueError(f"Object creation function {object_creation_func} is already in objects list.")

