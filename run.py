import arcade
from objects.player import Player
from engine.core import Engine
from engine.physics.object import PhysicsObject
from engine.physics.equations import drag_force

from CONSTANTS import (
                    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                    DEFAULT_SIDE
)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.eng = Engine()

        # add the player, which has a special on_update so it's
        # not made using the create_object function
        self.player = Player("resources/square.png", 1)
        # add it to the engine but don't have the engine update it
        # we do that ourselves in on_update
        self.eng.add_object(self.player, True, True)

        #self.eng.create_object(True, True, arcade_sprite="\"resources/square.png\",1",
        #                       PhysicsObject="x=50,y=50,static=True,has_collisions=False")

        # make some walls
        self.walls = []
        for x_coord in range(int(SCREEN_WIDTH/DEFAULT_SIDE)):
            args = "static=True,has_collisions=True,x=" + \
                str(x_coord*DEFAULT_SIDE) + ",y=" + str(DEFAULT_SIDE)
            self.walls.append(
                self.eng.create_object(
                    is_drawn=True, is_static=True, PhysicsObject=args)
            )
            args = "static=True,has_collisions=True,x=" + \
                str(x_coord*DEFAULT_SIDE) + ",y=" + \
                str(SCREEN_HEIGHT-DEFAULT_SIDE)
            self.walls.append(
                self.eng.create_object(
                    is_drawn=True, is_static=True, PhysicsObject=args)
            )

        for y_coord in range(int(SCREEN_HEIGHT/DEFAULT_SIDE)):
            args = "static=True,has_collisions=True,y=" + \
                str(y_coord*DEFAULT_SIDE) + ",x=" + str(DEFAULT_SIDE)
            self.walls.append(
                self.eng.create_object(
                    is_drawn=True, is_static=True, PhysicsObject=args)
            )
            args = "static=True,has_collisions=True,y=" + \
                str(y_coord*DEFAULT_SIDE) + ",x=" + \
                str(SCREEN_WIDTH-DEFAULT_SIDE)
            self.walls.append(
                self.eng.create_object(
                    is_drawn=True, is_static=True, PhysicsObject=args)
            )

        self.keys = {
                    "W": False,
                    "A": False,
                    "S": False,
                    "D": False
                    }

    def on_draw(self):
        arcade.start_render()
        self.eng.draw_objects()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.keys["W"] = True
        elif key == arcade.key.S:
            self.keys["S"] = True
        elif key == arcade.key.A:
            self.keys["A"] = True
        elif key == arcade.key.D:
            self.keys["D"] = True
        elif key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
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
        if key == arcade.key.W:
            self.keys["W"] = False
        elif key == arcade.key.S:
            self.keys["S"] = False
        elif key == arcade.key.A:
            self.keys["A"] = False
        elif key == arcade.key.D:
            self.keys["D"] = False

    def on_update(self, delta_time):
        self.player.update(delta_time, self.keys)

        #self.eng.physics_engine.apply_universal_force_func(
        #   drag_force, in_class=PhysicsObject)

        self.eng.update_objects(delta_time)


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
