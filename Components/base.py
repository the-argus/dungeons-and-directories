# name should not use the word "Component"
class Base():
    def __init__(self):
        # name variable , is just the name of the class
        self.name = self.__class__.__name__
        # gameobject component is attached to
        self.parent = None