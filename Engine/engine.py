import arcade
import os
import pymunk
import GameObjects as GO
from .key_manager import KeyManager

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

    def setup(self):
        """ Set up the game and initialize the variables. """
        
        self.global_sprite_list = arcade.SpriteList()
        
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=GLOBAL_DAMPING)

        self.keys = KeyManager()

    def on_draw(self):
        arcade.start_render()
        self.physics_engine.resync_sprites()
        self.global_sprite_list.draw()

    def on_key_press(self, key, modifiers):
        self.keys.on_key_press(key, modifiers)

        if key == arcade.key.F and modifiers & arcade.key.MOD_CTRL:
            # toggle fullscreen
            self.set_fullscreen(not self.fullscreen)

            # modify viewport to match fullscreen resolution
            width, height = self.get_size()
            if self.fullscreen:
                if SCREEN_WIDTH > SCREEN_HEIGHT:
                    aspect_ratio = height/width
                    x1 = 0
                    x2 = SCREEN_WIDTH
                    y1 = 0
                    y2 = int(SCREEN_WIDTH*aspect_ratio)
                else:
                    aspect_ratio = width/height
                    x1 = 0
                    x2 = int(SCREEN_HEIGHT*aspect_ratio)
                    y1 = 0
                    y2 = SCREEN_HEIGHT
            else:
                x1 = 0
                x2 = SCREEN_WIDTH
                y1 = 0
                y2 = SCREEN_HEIGHT
            self.set_viewport(x1, x2, y1, y2)

    def on_key_release(self, key, modifiers):
        self.keys.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        self.player.control(self.keys, delta_time)
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
