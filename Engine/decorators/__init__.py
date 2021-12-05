from constants.engine import EVENTS
from functools import wraps
from inspect import getfullargspec
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
def on_control_pressed(*controls):
    def add_control_flag(func):
        # verify that the function takes two arguments: the control and the key manager
    # TODO: also make sure its bound
        if not len(getfullargspec(func).args) == 3:
            raise ValueError("on_control_pressed handlers must take two arguments: the control pressed and the key manager")
        wraps(func)
        func.__annotations__["on_control_pressed"] = controls
        return func
    return add_control_flag

def on_control_released(*controls):
    def add_control_flag(func):
        # verify that the function takes two arguments: the control and the key manager
    # TODO: also make sure its bound
        if not len(getfullargspec(func).args) == 3:
            raise ValueError("on_control_released handlers must take two arguments: the control pressed and the key manager")
        wraps(func)
        func.__annotations__["on_control_released"] = controls
        return func
    return add_control_flag

def on_update(func):
    # verify that the function takes one argument for delta time
    # TODO: also make sure its bound
    if not len(getfullargspec(func).args) == 2:
        raise ValueError("on_update handlers must take only one argument for delta_time.")
    wraps(func)
    func.__annotations__["on_update"] = True
    return func

__all__ = [on_control_pressed, on_update, on_control_released]# + [eval(e) for e in EVENTS]