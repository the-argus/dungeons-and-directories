import pymunk

def lerp(x1, x2, lerp_amount):
    return x1 + ( ( x2 - x1 ) * x1 )

def clamp(value, range):
    if not (isinstance(value, (int, float))):
        raise ValueError(f"Clamp not supported between type {type(value)} and {type(range[0])}")
    if not len(range) == 2:
        raise ValueError(f"range argument for clamp should be an iterable of length 2, got {len(range)}")
    if not (isinstance(range[0], (int, float)) and isinstance(range[1], (int, float))):
        raise ValueError(f"Clamp not supported between type {type(value)} and {type(range[0])} and {type(range[1])}")
    return max(min(value, range[1]), range[0])

def json_custom_keyword_parse(json_value, engine):
    """
    accept a string from a json object and convert it to
    specified other objects, such as "None" becoming a
    literal None.
    """

    # type handling
    if isinstance(json_value, list) or isinstance(json_value, tuple):
        # recurse for all the items in the list
        init = []
        for item in json_value:
            init.append(json_custom_keyword_parse(item, engine))
        if isinstance(json_value, tuple):
            init = tuple(init)
        return init
    elif isinstance(json_value, dict):
        # recurse for all key/value pairs
        init = json_value
        for key, value in json_value.items():
            init[key] = json_custom_keyword_parse(value, engine)
        return init
    elif not isinstance(json_value, str):
        return json_value

    if json_value == "None":
        return None
    elif json_value == "INFINITY":
        return float('inf')
    elif json_value == "ENGINE":
        return engine
    elif json_value == "PYMUNK_STATIC":
        return pymunk.Body.STATIC
    elif json_value == "PYMUNK_DYNAMIC":
        return pymunk.Body.DYNAMIC
    elif json_value == "PYMUNK_KINEMATIC":
        return pymunk.Body.KINEMATIC
    elif json_value == "NEW_PYMUNK_STATIC_BODY":
        return pymunk.Body(body_type=pymunk.Body.STATIC)
    elif json_value == "NEW_PYMUNK_DYNAMIC_BODY":
        return pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    elif json_value == "NEW_PYMUNK_KINEMATIC_BODY":
        return pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    

    # attempt to parse string as a constant
    try:
        imp, var = json_value.split(":")
        exec(f"from constants.{imp} import {var}")
        c = eval(var)
        return c
    except ImportError:
        #print(f"{var} from constants.{imp} not found")
        pass
    except ValueError:
        #print(f"Improperly formatted json constant {json_value}")
        pass
    
    return json_value