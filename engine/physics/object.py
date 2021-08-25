from tools import arcade_sprite, create_bitmask

import arcade

from CONSTANTS import (
                    AA_RECT, RECT, CIRCLE, POLYGON,
                    DEFAULT_MAT, DEFAULT_SIDE
)


class PhysicsObject(object):
    # used to describe the material of the hitbox
    class Body():
        def __init__(self, mat, vol):
            self.density = mat[0]
            self.restitution = mat[1]
            self.mass = self.density * vol
            self.imass = 1/self.mass

    class Hitbox():
        """
        This class exists only inside of a physics object.

        It does not have an x or y position because it just uses its parent's.

        Positions of all points in the hitbox are defined relative to its parent's center,
        which leads to some extra math but that's okay because it's easier and I haven't
        even tested this yet so why would I go that far to optimize it


        Types:

        RECT [angle=0, width=DEFAULT_SIDE, height=DEFAULT_SIDE]
        AA_RECT [width=DEFAULT_SIDE, height=DEFAULT_SIDE]
        CIRCLE [radius=DEFAULT_SIDE, angle=0]
        POLYGON [points=[(0, 1), (1, 0), (-1, 0)], angle = 0]

        """

        def __init__(self, parent_object, type=AA_RECT, **kwargs):
            if not (isinstance(parent_object, PhysicsObject)):
                raise TypeError(
                    "Parent object of hitbox must be a PhysicsObject")
            self.type = type
            self.parent = parent_object

            # assign specail variables for the more complex shapes
            if type == AA_RECT or type == RECT:
                # inheirit from arcade sprite image size to make my life easier

                if isinstance(parent_object, arcade_sprite):
                    self.width = parent_object.textures[0].width
                    self.height = parent_object.textures[0].height
                else:
                    self.width = kwargs.get('width', DEFAULT_SIDE)
                    self.height = kwargs.get('height', DEFAULT_SIDE)

                # additional stuff for rectangles
                if type == RECT:
                    self.angle = 0
                    # get maximum diagonal length in case the rect is rotated
                    max_diag = (self.width**2 + self.height**2)**0.5
                    self.width = max_diag
                    self.height = max_diag
            elif type == CIRCLE:
                self.angle = 0
                self.radius = kwargs.get('radius', DEFAULT_SIDE)
                self.width = self.radius*2
                self.height = self.radius*2
            elif type == POLYGON:
                self.angle = 0
                # get the points that make up the polygon
                self.points = kwargs.get('points', [(0, 1), (1, 0), (-1, 0)])
                if not len(self.points) >= 3:
                    raise ValueError(
                        "Polygon hitboxes must be made up of three or more points.")

                # calculate width and height of the broad phase AABB by getting most distant points and using that for both
                max_distance = 0
                for point_a in self.points:
                    for point_b in self.points:
                        if not point_a is point_b:
                            dist = (point_b[0]-point_a[0])**2 + \
                                    (point_b[1]-point_a[1])**2
                            if dist > max_distance:
                                max_distance = dist
                self.width = max_distance
                self.height = max_distance
            else:
                raise TypeError("Unknown hitbox type.")

        def get_area(self):
            return self.width * self.height
    """
    Actual physics object
    """

    def __init__(self, **kwargs):
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        # default to a physics object that cant be collided with and can move
        self.has_collisions = kwargs.get('has_collisions', False)
        self.static = kwargs.get('static', False)

        layers = kwargs.get('layers', [])
        self.layers = create_bitmask(layers)

        if not self.static:
            self.fx = kwargs.get('x_force', 0)
            self.fy = kwargs.get('y_force', 0)
            self.vx = kwargs.get('vx', 0)
            self.vy = kwargs.get('vy', 0)

        self.hitbox = self.Hitbox(self, kwargs.get('hitbox_type', AA_RECT))

        # use the area of the hitbox plus the density to store mass in a body object
        self.body = PhysicsObject.Body(kwargs.get(
            'material', DEFAULT_MAT), self.hitbox.get_area())

        self.has_engine = False

        if kwargs.get('engine', None) is not None:
            kwargs.get('engine').add(self)

    def draw_hitbox(self, outline=False, color=arcade.color.RED):
        if self.hitbox.type == AA_RECT:
            if outline:
                draw = arcade.draw_rectangle_outline
            else:
                draw = arcade.draw_rectangle_filled
            draw(self.x, self.y, self.hitbox.width, self.hitbox.height, color)
        elif self.hitbox.type == CIRCLE:
            if outline:
                draw = arcade.draw_circle_outline
            else:
                draw = arcade.draw_circle_filled
            draw(self.x, self.y, self.hitbox.radius, color)
        else:
            if self.hitbox.type == RECT:
                w_2 = self.hitbox.width/2
                h_2 = self.hitbox.height/2
                point_list = ((self.x-w_2, self.y-h_2), (self.x+w_2, self.y-h_2),
                              (self.x+w_2, self.y+h_2), (self.x-w_2, self.y+h_2)
                              )
            else:
                point_list = tuple(self.points)

            if outline:
                draw = arcade.draw_polygon_outline
            else:
                draw = arcade.draw_polygon_filled

            draw(point_list, color)

    def enact_force(self, force):

        if self.static:
            raise TypeError("Force cannot be enacted on a static object")
            return None
        try:
            if (True, True) == (isinstance(force[0], (int, float)), isinstance(force[1], (int, float))):
                self.fx += force[0]
                self.fy += force[1]
            else:
                raise TypeError("Force must be numerical")
        except TypeError:
            raise TypeError(
                "The x and y components of force must be given as items in an iterable")
