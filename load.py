import pyglet

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

MISSING_TEX = pyglet.resource.image("missing_tex.png").get_texture()

blue_square = pyglet.resource.image("square.png")