import arcade
import math
from physics_demo.tools import sign, is_type_of, create_bitmask, bitmask_overlap
from physics_demo.collisions import simple_collide, complex_collide

from CONSTANTS import (
                        DEFAULT_SIDE, DEFAULT_MAT,
                        AA_RECT, RECT, CIRCLE, POLYGON,
                        FRAMERATE,
                        LAYERS
)


class PhysicsObject():
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

        self.hitbox = kwargs.get('hitbox', Hitbox(self, AA_RECT))

        # use the area of the hitbox plus the density to store mass in a body object
        self.body = PhysicsObject.Body(kwargs.get(
            'material', DEFAULT_MAT), self.hitbox.get_area())

        self.has_engine = False

        if kwargs.get('engine', None) is not None:
            kwargs.get('engine').add(self)

    def enact_force(self, force):
        def local_run():
            self.fx += force[0]
            self.fy += force[1]

        if self.static:
            raise TypeError("Force cannot be enacted on a static object")
            return None
        try:
            if (True, True) == (isinstance(force[0], (int, float)), isinstance(force[1], (int, float))):
                local_run()
            else:
                raise TypeError("Force must be numerical")
        except TypeError:
            raise TypeError(
                "The x and y components of force must be given as items in an iterable")

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
    even tested this yet so why would I go that far to optimize it.


    Types:

    RECT [angle=0, width=DEFAULT_SIDE, height=DEFAULT_SIDE]
    AA_RECT [width=DEFAULT_SIDE, height=DEFAULT_SIDE]
    CIRCLE [radius=DEFAULT_SIDE, angle=0]
    POLYGON [points=[(0, 1), (1, 0), (-1, 0)], angle = 0]

    """

    def __init__(self, parent_object, type=AA_RECT, **kwargs):
        if not (isinstance(parent_object, PhysicsObject) or issubclass(parent_object, PhysicsObject)):
            raise TypeError("Parent object of hitbox must be a PhysicsObject")
        self.type = type
        self.parent = parent_object

        # assign specail variables for the more complex shapes
        if type == AA_RECT:
            # inheirit from arcade sprite image size to make my life easier

            #if (isinstance(parent_object, arcade.sprite.Sprite) or issubclass(parent_object, arcade.sprite.Sprite)):
            if isinstance(parent_object, arcade.sprite.Sprite):
                self.width = parent_object.textures[0].width
                self.height = parent_object.textures[0].height
            else:
                self.width = kwargs.get('width', DEFAULT_SIDE)
                self.height = kwargs.get('height', DEFAULT_SIDE)
        elif type == RECT:
            self.angle = 0
            # get unrotated width and height
            if (isinstance(parent_object, arcade.sprite.Sprite) or issubclass(parent_object, arcade.sprite.Sprite)):
                self.width = kwargs.get(
                    'width', parent_object.textures[0].width)
                self.height = kwargs.get(
                    'height', parent_object.textures[0].height)
            else:
                self.width = kwargs.get('width', DEFAULT_SIDE)
                self.height = kwargs.get('height', DEFAULT_SIDE)
                # get maximum diagonal length in case the rect is roatated
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


class PhysicsEngine():
    def __init__(self):
        self.dynamics = []
        self.statics = []
        self.colliders = []

    def step(self, delta_time):
        def get_acceleration(object):
            acc = (object.fx*object.body.imass, object.fy*object.body.imass)
            # reset forces so they need to be reapplied
            object.fx = 0
            object.fy = 0
            return acc

        for object in self.dynamics:
            ax, ay = get_acceleration(object)
            object.vx += ax*delta_time/FRAMERATE
            object.vy += ay*delta_time/FRAMERATE
            self.move(delta_time, object)

    def move(self, delta_time, object):
        vx = object.vx*(delta_time/FRAMERATE)
        vy = object.vy*(delta_time/FRAMERATE)
        collided = False
        hit_objects = []
        for body in self.colliders:
            if bitmask_overlap(body.layers, object.layers):
                continue
            if simple_collide(object, body, (vx, vy)):
                collided = True
                hit_objects.append(body)
        if not collided:
            object.x += math.floor(vx)
            object.y += math.floor(vy)
            return

        #narrow phase, if did collide
        x_collided = False
        y_collided = False
        simple = object.hitbox.type == AA_RECT
        hit_complex = not simple
        x_cache = 0
        collided = False

        while (not collided) and abs(x_cache) < abs(vx):
            increment = sign(vx)
            for body in hit_objects:
                collision = simple_collide(
                    object, body, (x_cache + increment, 0))
                if collision:
                    collided = True
                    break
            # handle collision
            if not collided:
                x_cache += increment
            else:
                if not (body.hitbox.type == AA_RECT and simple):
                    hit_complex = True

                x_collided = True
                break

        object.x = int(object.x) + int(x_cache)

        # narrow phase again but y values this time
        y_cache = 0
        collided = False
        while (not collided) and abs(y_cache) < abs(vy):
            increment = sign(vy)
            for body in hit_objects:
                collision = simple_collide(
                    object, body, (0, y_cache + increment))
                if collision:
                    collided = True
                    break
            # handle collision
            if not collided:
                y_cache += increment
            else:
                if not (body.hitbox.type == AA_RECT and simple):
                    hit_complex = True

                y_collided = True
                break

        object.y = int(object.y) + int(y_cache)

        if (not simple) or hit_complex:
            self.complex_move(delta_time, object,
                              hit_objects, (x_cache, y_cache))
        else:
            if x_collided:
                object.vx = 0
            if y_collided:
                object.vy = 0

    def complex_move(self, delta_time, object, hit_objects, moved):
        # identical to regular move but can do complex collisions

        x_cache = 0
        collided = False

        vx = (object.vx-moved[0])*(delta_time/FRAMERATE)
        vy = (object.vy-moved[1])*(delta_time/FRAMERATE)

        while (not collided) and abs(x_cache) < abs(vx):
            increment = sign(vx)
            for body in hit_objects:
                collision = complex_collide(
                    object, body, (increment, 0))
                if collision:
                    collided = True
                    object.vx = 0
                    break
            # handle collision
            if not collided:
                x_cache += increment
            else:
                break

        object.x = int(object.x) + int(x_cache)

        # narrow phase again but y values this time
        y_cache = 0
        collided = False
        while (not collided) and abs(y_cache) < abs(vy):
            increment = sign(vy)
            for body in hit_objects:
                collision = complex_collide(
                    object, body, (0, increment))
                if collision:
                    collided = True
                    object.vy = 0
                    break
            # handle collision
            if not collided:
                y_cache += increment
            else:
                break

        object.y = int(object.y) + int(y_cache)

    def add(self, object):
        if is_type_of(object, PhysicsObject) and not object.has_engine:
            object.has_engine = True
            if object.static:
                self.statics.append(object)
            else:
                self.dynamics.append(object)
            if object.has_collisions:
                self.colliders.append(object)
        else:
            if not is_type_of(object, PhysicsObject):
                raise TypeError(
                    "Only a physics object can be added to an engine.")
            else:
                raise Exception("Physics object "
                                + str(object) + "is already in an engine.")

    def remove(self, object):
        """
        known issue: need to make sure the object was actually in the list before setting has engine to false
        """
        if object.static:
            self.statics.remove(object)
            object.has_engine = False
        else:
            self.dynamics.remove(object)
            object.has_engine = False

        if object.has_collisions:
            self.colliders.remove(object)
            object.has_engine = False
