import arcade
from physics_demo.player import Player, Wall
from physics_demo.core import PhysicsEngine
from CONSTANTS import (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    SCREEN_TITLE,
                    DEFAULT_SIDE
)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.engine = PhysicsEngine()

        self.player = Player()
        self.engine.add(self.player)

        self.walls = []

        # initialize a square of walls
        for i in range(int(SCREEN_WIDTH/DEFAULT_SIDE)):
            wall = Wall(y=DEFAULT_SIDE, x=i*DEFAULT_SIDE)
            self.engine.add(wall)
            self.walls.append(wall)

            wall = Wall(y=i*DEFAULT_SIDE, x=DEFAULT_SIDE)
            self.engine.add(wall)
            self.walls.append(wall)

            wall = Wall(y=SCREEN_HEIGHT-DEFAULT_SIDE,
                        x=SCREEN_WIDTH - (i*DEFAULT_SIDE))
            self.engine.add(wall)
            self.walls.append(wall)

            wall = Wall(y=SCREEN_HEIGHT-(i*DEFAULT_SIDE),
                        x=SCREEN_WIDTH-DEFAULT_SIDE)
            self.engine.add(wall)
            self.walls.append(wall)

        self.keys = {
                    "W": False,
                    "A": False,
                    "S": False,
                    "D": False
                    }

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        for wall in self.walls:
            wall.draw()

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
        self.engine.step(delta_time)


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
