from CONSTANTS import AA_RECT, RECT, POLYGON, CIRCLE
from physics_demo.tools import sign


def aabb_collide(width_1, height_1, x1, y1, width_2, height_2, x2, y2):
    h1_div = height_1/2
    h2_div = height_2/2
    w1_div = width_1/2
    w2_div = width_2/2
    x_satisfied = ((x1 + w1_div) > (x2 - w2_div)
                   and (x1 - w1_div) < (x2 + w2_div))
    y_satisfied = ((y1 + h1_div) > (y2 - h2_div)
                   and (y1 - h1_div) < (y2 + h2_div))
    return x_satisfied and y_satisfied


def circle_aabb_collide(c_rad, c_x, c_y, b_x, b_y, b_w, b_h):
    v_center = [c_x-b_x, c_y-b_y]
    #clamp the vector between the centers to get edge point coordinates
    if abs(v_center[0]) > b_w/2:
        v_center[0] = (b_w/2)*sign(v_center[0])
    if abs(v_center[1]) > b_h/2:
        v_center[1] = (b_h/2)*sign(v_center[1])

    edge_point = (b_x + v_center[0], b_y + v_center[1])

    if (c_x-edge_point[0])**2 + (c_y-edge_point[1])**2 <= c_rad**2:
        return True
    return False


def circle_circle_collide(x_1, y_1, x_2, y_2, rad_1, rad_2):
    min_dist = rad_1 + rad_2
    dist = (x_2-x_1)**2 + (y_2-y_1)**2
    return dist <= min_dist


# some easier use versions of the physics functions in collisions.py
def simple_collide(object1, object2, translation):
    return aabb_collide(object1.hitbox.width, object1.hitbox.height,
                        object1.x + translation[0], object1.y + translation[1],
                        object2.hitbox.width, object2.hitbox.height,
                        object2.x, object2.y
                        )


def complex_collide(object1, object2, translation):
    def circle_collide(object1, object2, translation):
        # collision if both objects are circles
        x_1 = object1.x + translation[0]
        y_1 = object1.y + translation[1]
        x_2 = object2.x
        y_2 = object2.y
        return circle_circle_collide(x_1,y_1,x_2,y_2,object1.hitbox.radius,object2.hitbox.radius)

    def polygon_collide(object1, object2, translation):
        # collision if both objects are polygons
        pass

    # complex collisions, hitbox types listed in order
    def circle_to_poly(object1, object2, translation):
        pass

    def circle_to_bbox(object1, object2, translation):
        if object1.hitbox.type == CIRCLE:
            c_coords = [object1.x + translation[0], object1.y + translation[1]]
            b_coords = [object2.x, object2.y]
            rad = object1.hitbox.radius
            width = object2.hitbox.width
            height = object2.hitbox.height
        else:
            c_coords = [object2.x, object2.y]
            b_coords = [object1.x + translation[0], object1.y + translation[1]]
            rad = object2.hitbox.radius
            width = object1.hitbox.width
            height = object1.hitbox.height

        return circle_aabb_collide(rad, c_coords[0], c_coords[1], b_coords[0], b_coords[1], width, height)

    def poly_to_bbox(object1, object2, translation):
        pass

    collision_function = simple_collide

    # makes later code more readable because we gotta do this over and over
    object1_is_poly = (object1.hitbox.type
                       == RECT or object1.hitbox.type == POLYGON)
    object2_is_poly = (object2.hitbox.type
                       == RECT or object2.hitbox.type == POLYGON)

    if object1_is_poly and object2_is_poly:
        collision_function = polygon_collide
    elif object1.hitbox.type == CIRCLE and object2.hitbox.type == CIRCLE:
        collision_function = circle_collide

    # if the objects are of different types
    else:
        if object1_is_poly or object2_is_poly:
            if object1.hitbox.type == CIRCLE or object2.hitbox.type == CIRCLE:
                collision_function = circle_to_poly
            else:
                collision_function = poly_to_bbox
        elif object1.hitbox.type == CIRCLE or object2.hitbox.type == CIRCLE:
            collision_function = circle_to_bbox

    return collision_function(object1, object2, translation)
