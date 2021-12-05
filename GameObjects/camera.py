import Components as C

def Camera(engine):
    c = engine.GameObject()

    c.add_component(C.Fullscreen(engine))

    return c