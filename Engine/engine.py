import arcade
import os
import pymunk
import GameObjects as GO
from .key_manager import KeyManager
from .scene import Scene

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
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)
        self.background_color = arcade.color.BLACK

        self.global_sprite_list = None

        self.physics_engine = None

        self.keys = None

        self._on_update_handlers = set()

        self._on_draw_handlers = set()

    def setup(self):
        """ Set up the game and initialize the variables. """
        
        self.global_sprite_list = arcade.SpriteList()
        
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=GLOBAL_DAMPING)

        self.keys = KeyManager()

    def on_draw(self):
        arcade.start_render()
        self.physics_engine.resync_sprites()
        self.global_sprite_list.draw()
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
        self.global_sprite_list.update()
    
    def GameObject(self, *args, object_class = GO.GameObject, **kwargs):
        """Create gameobject with reference to this engine."""
        obj = object_class(self, *args, **kwargs)

        # register with sprite list(s)
        # TODO: add layers, each with a set of sprite lists for static and dynamic bodies
        if isinstance(obj, arcade.Sprite):
            self.global_sprite_list.append(obj)

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
    
    def load(self, scene_init):
        scene = scene_init()
        
        # add physics bodies
        for body, shape in scene.physics_objects:
            self.physics_engine.space.add(body, shape)
        
        # create objects
        for object in scene.objects:
            object(self)