
def json_custom_keyword_parse(string, engine):
    """
    accept a string from a json object and convert it to
    specified other objects, such as "None" becoming a
    literal None.
    """
    if string == "None":
        return None
    elif string == "INFINITY":
        return float('inf')
    elif string == "ENGINE":
        return engine
    

    # attempt to parse string as a constant
    try:
        imp, var = string.split(":")
        exec(f"from constants.{imp} import {var}")
        c = eval(var)
        return c
    except ImportError:
        print(f"{var} from constants.{imp} not found")
        pass
    
    return string