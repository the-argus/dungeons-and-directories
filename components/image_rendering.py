from ctypes import ArgumentError
import pyglet
from pyglet.gl import GL_TRIANGLES, GL_QUADS
from tools import IDDict
from CONSTANTS import DEFAULT_LAYER, DEFAULT_USAGE
from load import MISSING_TEX

"""
The goal of this file is to create a manager which contains references to the information
inside of pyglet draw batches. All information is organized into dicts by unique id.
It should render the concept of creating pyglet sprites useless, and replace it with direct
modification of the draw batch information.
"""

class BatchHandler():
    def __init__(self, engine):

        # TODO: implement arcade's spatial hashing and add multiple batches for different
        # batches with different amounts of hashing.
        # Also add "offset" for if the texture shouldn't display over the sprite's anchor
        # point.
        self._batch = pyglet.graphics.Batch()

        # sprite's info, all by id
        self._texture = IDDict(engine)
        self._vertex_list = IDDict(engine)

    def _create_vertex_list(self, coords, usage=DEFAULT_USAGE, color=[255,255,255,255], scale=1, rotation=0, group = DEFAULT_LAYER, texture = MISSING_TEX):
        """
        Create a new vertex list with the given vertex info.

        :coords: Tuple (x, y)

        :scale: int. currently does nothing

        :rotation: float. currently does nothing

        Return the vertex list.
        """

        tex_coords = texture.tex_coords
        """
        # new code, up to date with what's on pyglet github (pyglet 2.0-dev9)
        vertex_list = self._batch.add_indexed(
            4, GL_TRIANGLES, group, [0, 1, 2, 0, 2, 3],
            'position2f/%s' % usage,
            ('colors4Bn/%s' % usage, tuple(color) * 4),
            ('translate2f/%s' % usage, tuple(coords) * 4),
            ('scale2f/%s' % usage, (scale, scale) * 4),
            ('rotation1f/%s' % usage, (rotation,) * 4),
            ('tex_coords3f/%s' % usage, tex_coords))
        """
        vertex_format = 'v2i/%s' % usage
        vertex_list = self._batch.add(
                4, GL_QUADS, group, vertex_format, 'c4B', ('t3f', texture.tex_coords))

        self._match_position_to_texture(vertex_list=vertex_list, texture=texture)
        self._update_vlist_color(vertex_list=vertex_list, color=color[:2], opacity=color[3])

        return vertex_list
    
    def _match_position_to_texture(self, vertex_list, texture):
        """
        Adjust vertices of vertex list to be the size of a texture.
        TODO: add support for rotation and scale.
        """

        x1 = -texture.anchor_x
        y1 = -texture.anchor_y
        x2 = x1 + texture.width
        y2 = y1 + texture.height
        vertices = (x1, y1, x2, y1, x2, y2, x1, y2)
        """
        vlist.position[:] = tuple(map(int, verticies))
        """
        vertices = (int(vertices[0]), int(vertices[1]),
                    int(vertices[2]), int(vertices[3]),
                    int(vertices[4]), int(vertices[5]),
                    int(vertices[6]), int(vertices[7]))
        vertex_list.vertices[:] = vertices
    
    def _update_vlist_color(self, vertex_list, color, opacity):
        vertex_list.colors[:] = [*color, int(opacity)] * 4

    def add_sprite(self, object, **kwargs):
        """Add sprite information into the draw batch. Overwrites existing sprite info."""
        identifier = object.id
        try:
            self._texture[identifier] = kwargs["texture"]
        except KeyError:
            pass
        
        self._vertex_list[identifier] = self._create_vertex_list(object.coords, **kwargs)
    
    def _update_object_color(self, identifier, color):
        self._color[identifier] = color
    
    def draw(self):
        self._batch.draw()
