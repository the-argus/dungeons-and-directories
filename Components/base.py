# name should not use the word "Component"
class Base():
    def __init__(self):
        # name variable , is just the name of the class
        self.name = self.__class__.__name__
        # gameobject component is attached to
        self.parent = None
    
    def _attached(self):
        """init called after this object recieves a parent"""
        pass
    
    def cleanup(self):
        """Called whenever this component is removed from a GameObject"""
        pass

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
        if value is not None:
            self._attached()