import arcade

from CONSTANTS import (
                        DEFAULT_SIDE, DEFAULT_MAT,
                        AA_RECT, RECT, CIRCLE, POLYGON
)

class PhysicsObject():
    def __init__(self, **kwargs):
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        # default to a physics object that cant be collided with and can move
        self.has_collisions = kwargs.get('has_collisions', False)
        self.static = kwargs.get('static', False)
        
        if not self.static:
            self.fx = kwargs.get('x_force', 0)
            self.fy = kwargs.get('y_force', 0)
            self.vx = kwargs.get('vx', 0)
            self.vy = kwargs.get('vy', 0)
        
        self.hitbox = kwargs.get('hitbox', Hitbox(self, AA_RECT))
        
        # use the area of the hitbox plus the density to store mass in a body object
        self.body = PhysicsObject.Body(kwargs.get('material', DEFAULT_MAT), self.hitbox.get_area())
        
        self.has_engine = False
    def enact_force(self, force):
        def local_run():
            self.fx += force[0]
            self.fy += force[1]
        
        if self.static:
            raise TypeError("Force cannot be enacted on a static object")
            return None
        try:
            if (True, True) == (isinstance(force[0],(int, float)), isinstance(force[1],(int, float))):
                local_run()
            else:
                raise TypeError("Force must be numerical")
        except TypeError:
            raise TypeError("The x and y components of force must be given as items in an iterable")

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
                self.width = kwargs.get('width', parent_object.textures[0].width)
                self.height = kwargs.get('height', parent_object.textures[0].height)
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
                raise ValueError("Polygon hitboxes must be made up of three or more points.")
            
            # calculate width and height of the broad phase AABB by getting most distant points and using that for both
            max_distance = 0
            for point_a in self.points:
                for point_b in self.points:
                    if not point_a is point_b:
                        dist = (point_b[0]-point_a[0])**2 + (point_b[1]-point_a[1])**2
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
    def step(self):
        def get_acceleration(object):
            acc = (object.fx*object.body.imass, object.fy*object.body.imass)
            # reset forces so they need to be reapplied
            object.fx = 0
            object.fy = 0
            return acc

        for object in self.dynamics:
            ax, ay = get_acceleration(object)
            object.vx += ax
            object.vy += ay
            self.move(object)
    def move(self, object):
        vx = object.vx
        vy = object.vy
        x = object.x
        y = object.y
        collided = False
        for body in self.colliders:
            if aabb_collide(object.width, object.height, x+vx, y+vy, body.width, body.height, body.x, body.y):
                collided = True
        if not collided:
            object.x += object.vx
            object.y += object.vy
            return
        
        # this was prematurely optimized, got rid of it and made something more basic
        # also for some reason i forgot this function already had the dynamic object as an argument
        # and i don't need to loop through dynamics again
        """
        def distance(object1, object2):
            return (object2.x - object1.x)**2 + (object2.y - object1.y)**2
        
        for body in self.dynamics:
            if body in self.colliders:
                temp_list = self.colliders.remove(body)
            else:
                temp_list = self.colliders
            temp_list = quicksort_distance(temp_list)
            for collider in temp_list if distance(body, collider) <
        """
            
    def add(self, object):
        if (isinstance(object, PhysicsObject) or issubclass(object, PhysicsObject)) and not object.has_engine:
            object.has_engine = True
            if object.static:
                self.statics.append(object)
            else:
                self.dynamics.append(object)
            if object.has_collisions:
                self.colliders.append(object)
        else:
            if not (isinstance(object, PhysicsObject) or issubclass(object, PhysicsObject)):
                raise TypeError("Only a physics object can be added to an engine.")
            else:
                raise Exception("Physics object " + str(object) + "is already in an engine.")
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
    
    # old prematurely optimized collision stuff
    """
    def quicksort_distance(self, list, center):
        # this distance function can be given that decorator that makes it
        # remember past outputs but idk what it is an I dont have internet
        def distance(object):
            return (object.x - center[0])**2 + (object.y - center[1])**2
        def quicksort(list):
            object_list = list[:]
            if object_list == []:
                return []
            else:
                pivot = object_list[0]
                lesser = quicksort([x for x in object_list[1:] if distance(x) < pivot])
                greater = quicksort([x for x in object_list[1:] if distance(x) >= pivot])
                object_list = lesser + [pivot] + greater
                return object_list
        return quicksort(list)
    """

def aabb_collide(width_1, height_1, x1, y1, width_2, height_2, x2, y2):
    h1_div = height_1/2
    h2_div = height_2/2
    w1_div = width_1/2
    w2_div = width_2/2
    x_satisfied = ((x1 + w1_div) > (x2 - w2_div) and (x1 - w1_div) < (x2 + w2_div))
    y_satisfied = ((y1 + h1_div) > (y2 - h2_div) and (y1 - h1_div) < (y2 + h2_div))
    return x_satisfied and y_satisfied
        