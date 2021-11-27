
# the name of functions who should have decorators by the same name
# ie there should be a decorator @on_draw which causes that function
# (provided its in a component) to be run every on_draw
EVENTS = [
    "on_update",
    "on_draw",
    "on_mouse_motion",
    "on_mouse_press",
    "on_mouse_drag",
    "on_mouse_release",
    "on_mouse_scroll",
    "on_key_press",
    "on_key_release",
    "on_resize"
]