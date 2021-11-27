from constants.engine import EVENTS
from functools import wraps
from copy import copy, deepcopy
"""
# custom function decorators which add a leetle flag to the functions dictionary
for event in EVENTS:
    def base_event(func):
        wraps(func)
        if not func.__dict__.has_key("decorator_flags"):
            func.__dict__["decorator_flags"] = set()
        func.__dict__["decorator_flags"].add(event)
        return func
    # jank eval thing to declare the functions
    dec = event + " = base_event"
    eval(dec)
    # remove the originally created function
    del base_event
"""
# decorators that take specified arguments (manually declared)
# uses set of flags inside a functions dict called argument_decorator_flags
def on_control_pressed(control_list):
    def add_control_flag(f):
        print(dir(f.__dict__))
        func = deepcopy(f)
        wraps(func)
        for control in control_list:
            # flag value tuple marks what kind of decorator it is
            get = getattr(func, "argument_decorator_flags", None)
            if get is None:
                get = set()
            setattr(func, "argument_decorator_flags", get.add(control))
        return func
    return add_control_flag

__all__ = [on_control_pressed]# + [eval(e) for e in EVENTS]