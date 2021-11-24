import math
import inspect
from random import randint
from CONSTANTS import MAX_ID_ITERATIONS

"""
This file contains a ton of random reusable stuff.
"""
class IDDict(dict):
    """
    Dictionary that adds itself to an engine's references whenever it's created,
    and has a default value.
    """
    def __init__(self, engine=None, default=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # i could override .get to use this instead of None
        # but idk overriding native classes is weird, dont
        # wanna have to debug that rn
        self.default = default
        if engine is not None:
            engine.references.append(self)


def get_unique_id(used : dict) -> str:
    """Return a unique string given used unique strings."""
    #TODO: Make this better. Bad things could happen when the used id dict starts to get full
    key = randint(0,2000000)
    iters = 0
    while (used.get(key) != None):
        key = randint(0,2000000)
        iters += 1
        if iters > MAX_ID_ITERATIONS:
            raise Exception("Maximum ID generation iterations reached, no ID generated.")
    return str(key)

# stolen from le stack overflow
def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

def spritelist_key(spritelist):
    """Return a string of numbers seeded on arcade spritelist characteristics."""
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


def sign(num):
    if num == 0:
        return 0
    else:
        return num/abs(num)

