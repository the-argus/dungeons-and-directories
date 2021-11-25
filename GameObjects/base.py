import arcade
import Components

class GameObject():
    def __init__(self):
        # components dict contains lists of instances of a given component tied to this object, 
        self._components = {}

    def add_component(self, component : Components.Base, index=-1) -> int:
        """Append component to this object's list of components of the same type. Return index in list.
        NOTE: using index could be really bad because you could fuck up any indices of other objects you may have stored.
        It's there if you need it I guess"""

        try:
            if component not in self._components[component.name]:
                # append/insert object to list
                self._components[component.name].insert(component, index)
                component.parent = self
                placement = index if (index != -1) else len(self._components[component.name])
            else:
                raise ValueError(f"GameObject {self} already contains component {component} of type {component.name}.")
        except KeyError:
            # value doesnt exist yet, create new sublist for components of this type
            self._components[component.name] = [component]
            component.parent = self
            placement = 0
        
        # add references to all the component's functions for ease of access and override stuff
        # jank city. probably should probably add flags to functions instead of looking for the __, but this is easier for now
        newfs = {v:getattr(component, v) for v in dir(component) if callable(getattr(component, v)) and v[:2] != "__"}

        for name, function in newfs.items():
            self.__dict__[name] = function
            # TODO: google how to use logging lol
            # print(f"Added function {name} to {self}.")

        return placement
    
    def remove_component(self, component, index=-1) -> None:
        """ Remove a component from this object's components dict. Accepts component names, components names + index,
            or specific component objects."""
        if isinstance(component, str):
            # remove first component of name "component"
            try:
                self._components[component.name].pop(index)
                if self._components[component.name] == []:
                    self._components.pop(component.name)
            except ValueError:
                raise ValueError(f"GameObject {self} does not have any components under name {component}.")
            except IndexError:
                raise IndexError(f"GameObject {self}'s component list of {component}s does not contain index {index}.")
        elif isinstance(component, Components.Base):
            # remove the specific component passed in
            try:
                self._components[component.name].remove(component)
                if self._components[component.name] == []:
                    self._components.pop(component.name)
            except ValueError:
                # NOTE: valueerror could come from either the _components dict lookup OR remove, depend on where it doesnt exist.
                raise ValueError(f"Specific Component {component} not found in GameObject {self}.")
        else:
            raise ValueError(f"Uknown type for {remove_component} argument \"component\"")
    
    def Component(self, component : str, index=0):
        """Retrieve component from this game object by name and, optionally, index."""
        try:
            if isinstance(component, str):
                return self._components[component][index]
            elif isinstance(component, Components.Base):
                return self._components[component.name][index]
            else:
                # failstate, maybe component is the component type and not an instance?
                return self._components[component.__name__][index]
        except KeyError:
            # raise ValueError(f"GameObject {self} does not have any components of type {component}")
            return None
        except IndexError:
            raise IndexError(f"Index {index} is out of range of GameObject {self}'s list of {component} components.")

class GameObjectVisible(arcade.Sprite, GameObject):
    """
    Multiple inheiritance passthrough class thing.
    Probably should just be replaced by not drawing
    a game object.
    """
    def __init__(self, *args, **kwargs):
        # combine sprite init
        arcade.Sprite.__init__(self, *args, **kwargs)
        # with gameobject init
        GameObject.__init__(self)
