import arcade
# dont import other stuff please, dir() is used in this file

"""
key modifier constants for reference:
MOD_SHIFT
MOD_CTRL
MOD_ALT         Not available on Mac OS X
MOD_WINDOWS     Available on Windows only
MOD_COMMAND     Available on Mac OS X only
MOD_OPTION      Available on Mac OS X only
MOD_CAPSLOCK
MOD_NUMLOCK
MOD_SCROLLLOCK
MOD_ACCEL       Equivalent to MOD_CTRL, or MOD_COMMAND on Mac OS X.

these are all bitmasks, so to test for a modifier youd do:

if modifier & MOD_CTRL:
    do thing

to define multiple modifier for one key, do MOD1 | MOD2 | MOD3 ...
if fullscreen was CTRL + SHIFT + F:
FULLSCREEN = {arcade.key.F : arcade.key.MOD_CTRL | arcade.key.MOD_SHIFT}
"""

# possible keys are in dicts in format key : modifiers
# I guess you could say theyre stored in KEY - value pairs amiright guys ahaha
FORWARD =   {arcade.key.W : 0, arcade.key.UP     : 0}
BACK    =   {arcade.key.S : 0, arcade.key.DOWN   : 0}
LEFT    =   {arcade.key.A : 0, arcade.key.LEFT   : 0}
RIGHT   =   {arcade.key.D : 0, arcade.key.RIGHT  : 0}
# no modifiers is 0

FULLSCREEN = {arcade.key.F : arcade.key.MOD_CTRL}

# make set of all possible keys
_ls = [eval(v) for v in dir() if v[:2] != "__" and v != 'arcade']
USED_KEYS = set()
USED_CONTROLS = _ls

for control in _ls:
    for key in control:
        USED_KEYS.add(key)