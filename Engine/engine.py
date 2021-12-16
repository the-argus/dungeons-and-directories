import arcade
import os
import pymunk
import json
import GameObjects as GO
from .key_manager import KeyManager
from .layer import Layer
from utils import json_custom_keyword_parse

from constants.screen import (  SCREEN_WIDTH,
                                SCREEN_HEIGHT,
                                SCREEN_TITLE
)
from constants.physics import ( WALL_FRICTION,
                                GLOBAL_DAMPING
)

class GameEngine(arcade.Window):
    """
    Class meant to manage registering objects with the physics engine
    and calling flagged component functions on inputs, updates, and draws.
    It should not contain any explicit loading or creating of objects.
    """
    def __init__(self, width, height, title, layers=3):
        super().__init__(width, height, title, antialiasing=False)
        self.background_color = arcade.color.BLACK

        self.layers = [Layer() for i in range(layers)]

        self.physics_engine = None

        self.keys = None

        self._on_update_handlers = set()

        self._on_draw_handlers = set()

        self.named_objects = {}

    def setup(self):
        """ Set up the game and initialize the variables. """
        
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=GLOBAL_DAMPING)

        self.keys = KeyManager()

    def on_draw(self):
        arcade.start_render()
        self.physics_engine.resync_sprites()
        for layer in self.layers:
            layer.draw()
        for handler in self._on_draw_handlers:
            handler()

    def on_key_press(self, key, modifiers):
        self.keys.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.keys.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        for handler in self._on_update_handlers:
            handler(delta_time)
        
        self.physics_engine.step(delta_time)

        for layer in self.layers:
            layer.update()
    
    def GameObject(self, *args, object_class=GO.GameObject, layer=0, use_spatial_hash=False, spatial_hash_cell_size=128, **kwargs):
        """Create gameobject with reference to this engine."""
        if isinstance(object_class, str):
            cl = eval(f"GO.{object_class}")
            obj = cl(self, *args, **kwargs)
        else:
            obj = object_class(self, *args, **kwargs)
        
        n = kwargs.get("name")
        if n is not None:
            obj.name = n

        # register with sprite list(s)
        if layer is None:
            layer = 0
        if isinstance(obj, arcade.Sprite) or isinstance(obj, arcade.Texture):
            self.layers[layer].add_sprite(obj, use_spatial_hash, spatial_hash_cell_size)
        
        if obj.name is not None:
            if self.named_objects.get(obj.name) is not None:
                # name must be unique atm
                raise ValueError(f"Multiple objects created with name \"{obj.name}\" have been created.")
            self.named_objects[obj.name] = obj

        return obj
    
    def register_handler(self, handler_func):
        # control event handlers, pass off to key manager
        ocp = handler_func.__annotations__.get("on_control_pressed")
        ocr = handler_func.__annotations__.get("on_control_released")
        if ocp:
            for control in ocp:
                self.keys.add_control_press_handler(handler_func, control)
        if ocr:
            for control in ocr:
                self.keys.add_control_release_handler(handler_func, control)
        
        if handler_func.__annotations__.get("on_draw"):
            self._on_draw_handlers.add(handler_func)
        
        if handler_func.__annotations__.get("on_update"):
            self._on_update_handlers.add(handler_func)
    
    def load(self, scene_path):
        """load a json scene into the game state"""
        
        with open(f"Scenes/{scene_path}.json", "r") as s:
            data = json_custom_keyword_parse(json.load(s), self)
        
        # load the game objects
        for obj_name in data.get("Objects",[]):
            GO.load_object(obj_name, self)
        
        bodies = []
        for obj in data.get("PhysicsObjects", {}).get("bodies", []):
            kwargs = obj.get("kwargs", {})
            body = pymunk.Body(**kwargs)
            bodies.append(body)
        
        for obj in data.get("PhysicsObjects", {}).get("shapes", []):
            # convert the body index to an actual reference if necessary
            body = obj["kwargs"]["body"]
            if isinstance(body, int):
                obj["kwargs"]["body"] = bodies[body]
                body = bodies[body]

            # create the shapes and bodies
            type = obj["type"]
            pymunk_class = eval(f"pymunk.{type}")
            shape = pymunk_class(**obj["kwargs"])

            self.physics_engine.space.add(body, shape)
