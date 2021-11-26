

# custom function decorators which add a leetle flag to the functions dictionary
def on_update(func):
    func.__dict__["__on_update__"] = True

def on_draw(func):
    func.__dict__["__on_draw__"] = True