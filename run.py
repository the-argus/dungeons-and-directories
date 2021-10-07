import pyglet
import pyglet.window.key as key
from load import blue_square

from engine.Engine import Engine
from CONSTANTS import (
                    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, Components, LAYERS
)

def main():
    """ Main method """
    window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    engine = Engine()
    keys = {
            key.W: False,
            key.A: False,
            key.S: False,
            key.D: False
            }
    
    # create player
    player = engine.create_object((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    engine.add_component(   player, Components.sprite_renderer,
                            texture=blue_square.get_texture(),
                            group=LAYERS["foreground"] )

    # window events
    @window.event
    def on_draw():
        window.clear()
        engine.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol in keys:
            keys[symbol] = True
    
    @window.event
    def on_key_release(symbol, modifiers):
        if symbol in keys:
            keys[symbol] = False



    pyglet.app.run()


if __name__ == "__main__":
    main()
