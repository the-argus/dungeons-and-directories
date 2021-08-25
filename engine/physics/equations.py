from CONSTANTS import DRAG
from tools import sign
from engine.physics.object import PhysicsObject


def drag_force(object) -> tuple:
    x_element = -sign(object.vx)*(DRAG*object.hitbox.width*(object.vx**2))/2
    y_element = -sign(object.vy)*(DRAG*object.hitbox.height*(object.vy**2))/2
    return (x_element, y_element)
