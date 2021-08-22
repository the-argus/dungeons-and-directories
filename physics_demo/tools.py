

def sign(num):
    if num == 0:
        return 0
    else:
        return num/abs(num)


def is_type_of(object, in_class):
    return (isinstance(object, in_class) or issubclass(type(object), in_class))


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
