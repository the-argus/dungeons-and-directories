import math
from random import randbytes
from CONSTANTS import MAX_ID_ITERATIONS

def get_unique_id(used : dict) -> str:
    """Return a unique string given used unique strings."""
    key = randbytes(4)
    iters = 0
    while (used.get(key, True)):
        key = randbytes(4)
        iters += 1
        if iters > MAX_ID_ITERATIONS:
            raise Exception("Maximum ID generation iterations reached, no ID generated.")
    return key



def spritelist_key(spritelist):
    """Return a string of numbers seeded on spritelist characteristics."""
    # use the characteristics of the sprite and append the bits together
    # potential for overlap if spatial hash cell size exceeds 2^8
    key = spritelist.spatial_hash.cell_size & 0b11111111
    key = key << 2
    key = set_bit(key, 1, spritelist.use_spatial_hash())
    key = set_bit(key, 0, spritelist.is_static)
    return str(key)

def set_bit(value, bit, on_off):
    num = value
    if on_off:
        # insert bit
        num |= (1<<bit)
    else:
        # set the bit to 0
        num & ~(1<<bit)
    return num

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

