from tools import arcade_sprite, read_kwargs
from arcade import SpriteList
from engine.physics.object import PhysicsObject
from objects.player import Player
from engine.physics.engine import PhysicsEngine


class Engine():
    def __init__(self):
        self.physics_engine = PhysicsEngine()
        self.dynamic_objects = []
        self.drawn_physics_objects = []
        self.drawn_arcade_objects = SpriteList()

    def create_object(self, is_drawn, is_static, **objects):
        """
        kwargs are the classes and their constructor arguments
        they are formed into a massive frankenstein class
        """

        # get just the keywords/class names
        inherits = (eval(ob) for ob in objects.keys())

        class GameObject(*inherits):
            def __init__(self):
                super().__init__()
                # perform the init function of all the parent classes
                for cls, parameters in objects.items():
                    if parameters == "":
                        eval(cls).__init__(self)
                    else:
                        evaluated = read_kwargs(parameters)
                        evaluated = {kw: eval(item)
                                     for (kw, item) in evaluated.items()}
                        eval(cls).__init__(self, **evaluated)

        # create the object and store it in the necessary lists for updating
        game_object = GameObject()
        self.add_object(game_object, is_static, is_drawn)

        return game_object

    def add_object(self, object, is_static, is_drawn):
        if is_drawn:
            if isinstance(object, arcade_sprite):
                self.drawn_arcade_objects.append(object)
            elif isinstance(object, PhysicsObject):
                self.drawn_physics_objects.append(object)
            else:
                raise TypeError(
                    str(object) + " is neither a PhysicsObject nor an arcade_sprite, and cannot be drawn by this engine.")
        if not is_static:
            self.dynamic_objects.append(object)
        if isinstance(object, PhysicsObject):
            self.physics_engine.add(object)

    def draw_objects(self):
        for object in self.drawn_arcade_objects.sprite_list:
            object.set_position(object.x, object.y)
        self.drawn_arcade_objects.draw(filter="JANK (not filtered)")
        for object in self.drawn_physics_objects:
            object.draw_hitbox()

    def update_objects(self, delta_time):
        for object in self.dynamic_objects:
            object.update(delta_time)
        self.physics_engine.step(delta_time)
