from arcade import Sprite
import math

# passthrough class


class arcade_sprite(Sprite):
    pass


def list_to_str(in_list):
    final = ""
    for char in in_list:
        if isinstance(char, str):
            final += char
        else:
            raise TypeError("Cannot concatenate non string types.")
    return final


def compass_atan(opposite, adjacent):
    """
    Inverse tangent but it's only accurate to the cardinal directions and diagonals.
    """
    if opposite == 0:
        if adjacent == 0:
            # this will never return unless both input are 0
            return 2*math.pi
        elif adjacent > 0:
            return 0
        else:
            return math.pi
    elif opposite > 0:
        if adjacent == 0:
            return math.pi/2
        elif adjacent > 0:
            return math.pi/4
        else:
            return 3*math.pi/4
    else:
        if adjacent == 0:
            return 3*math.pi/2
        elif adjacent > 0:
            return 7*math.pi/4
        else:
            return 5*math.pi/4
        
        

def read_kwargs(in_string):
    # takes a string and returns a dict which can be unpacked as kwargs
    # items in the dict are strings so they can be eval-ed outside
    final = {}
    current_kw = []
    current_item = []
    mode = current_kw

    for char in in_string:
        if char != "," and char != "=":
            mode.append(char)
        elif char == "=":
            mode = current_item
        elif char == " ":
            pass
        else:
            final[list_to_str(current_kw)] = list_to_str(current_item)
            current_kw = []
            current_item = []
            mode = current_kw

    final[list_to_str(current_kw)] = list_to_str(current_item)

    return final


def sign(num):
    if num == 0:
        return 0
    else:
        return num/abs(num)


def create_bitmask(bits: list) -> int:
    final = 0
    if bits is not None:
        for bit in bits:
            final += 2**bit
    return final


def bitmask_overlap(mask1: int, mask2: int) -> bool:
    return (mask1 & mask2) != 0
    """
    I didn't know bitwise operators existed, okay?
    # returns true if mask1 and mask2 both contain an element
    layer_1 = mask1
    layer_2 = mask2
    while layer_1 > 0 and layer_2 > 0:
        layer_1, has_bit_1 = divmod(layer_1, 2)
        layer_2, has_bit_2 = divmod(layer_2, 2)
        if has_bit_1 and has_bit_2:
            return True
    return False
    """


# unused
def get_binary(bitmask: int) -> list:
    num = bitmask
    binary = []
    while num > 0:
        div, mod = divmod(num, 2)
        num = div
        binary.append(mod)
    return binary[::-1]
