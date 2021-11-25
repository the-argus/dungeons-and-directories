import arcade
import os
import GameObjects as GO

from constants.screen import (  SCREEN_WIDTH,
                                SCREEN_HEIGHT,
                                SCREEN_TITLE
)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.global_sprite_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.keys = {
                    "W": False,
                    "A": False,
                    "S": False,
                    "D": False
                    }
        
        self.global_sprite_list = arcade.SpriteList()
        
        # example of constructing a game object
        self.physics_engine = arcade.PymunkPhysicsEngine()
        self.player = GO.Player(self.physics_engine)

        self.global_sprite_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.physics_engine.resync_sprites()
        self.global_sprite_list.draw()

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
            # toggle fullscreen
            self.set_fullscreen(not self.fullscreen)

            # modify viewport to match fullscreen
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
        self.player.control(self.keys, delta_time)
        self.physics_engine.step(delta_time)
        self.global_sprite_list.update()


def main():
    """ run when this script is executed """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

    # ian's jank window transparency fix. can be removed in actual releases, sorry lads
    try:
        os.system(f"xprop -name \"{SCREEN_TITLE}\" -format _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY $(printf 0x%x $((0xffffffff)))")
    except Exception:
        pass


if __name__ == "__main__":
    main()
