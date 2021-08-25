import math
from engine.physics.object import PhysicsObject
from engine.physics.collisions import simple_collide, complex_collide
from tools import sign, bitmask_overlap
from CONSTANTS import (
                    AA_RECT, RECT, CIRCLE, POLYGON,
                    FRAMERATE,
                    LAYERS

)


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

    def apply_universal_force_func(self, force_func, in_class=None, in_list=[]):
        """
        force should take a physics object and output a force (x, y) tuple
        """
        if in_class == None:
            if in_list == []:
                for object in self.dynamics:
                    object.enact_force(force_func(object))
            else:
                for object in in_list:
                    object.enact_force(force_func(object))
        else:
            if in_list == []:
                for object in self.dynamics:
                    if isinstance(object, in_class):
                        object.enact_force(force_func(object))
            else:
                for object in in_list:
                    if isinstance(object, in_class):
                        object.enact_force(force_func(object))

    def add(self, object):
        if isinstance(object, PhysicsObject) and not object.has_engine:
            object.has_engine = True
            if object.static:
                self.statics.append(object)
            else:
                self.dynamics.append(object)
            if object.has_collisions:
                self.colliders.append(object)
        else:
            if not isinstance(object, PhysicsObject):
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
