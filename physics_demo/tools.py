

def sign(num):
    if num == 0:
        return 0
    else:
        return num/abs(num)


def is_type_of(object1, object2):
    return (isinstance(object1, type(object2)) or issubclass(type(object1), type(object2)))
