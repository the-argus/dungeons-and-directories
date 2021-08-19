import arcade
import math

from CONSTANTS import (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    SCREEN_TITLE
)


class Player(arcade.Sprite):
    def __init__(self, sprite, scale):
        super().__init__(sprite, scale)
        self.vx = SCREEN_WIDTH/2
        self.vy = SCREEN_HEIGHT/2
        self.max_speed = 300
        self.move_force = 50
        self.drag = 0.3
        self.mass = 0.1

    def update(self, delta_time, keys):
        xin = keys["D"] - keys["A"]
        yin = keys["W"] - keys["S"]

        self.vx += (xin*self.move_force - self.vx
                    * self.drag)*delta_time/self.mass
        self.vy += (yin*self.move_force - self.vy
                    * self.drag)*delta_time/self.mass

        self.vx = min(self.vx, self.max_speed)
        self.vy = min(self.vy, self.max_speed)

        self.center_x += self.vx*delta_time
        self.center_y += self.vy*delta_time


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player = Player("resources/square.png", 1)

        self.keys = {
                        "W": False,
                        "A": False,
                        "S": False,
                        "D": False
                        }

    def on_draw(self):
        arcade.start_render()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.keys["W"] = True
        elif key == arcade.key.S:
            self.keys["S"] = True
        elif key == arcade.key.A:
            self.keys["A"] = True
        elif key == arcade.key.D:
            self.keys["D"] = True

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


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
