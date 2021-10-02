import arcade
from tools import spritelist_key, get_unique_id

class Engine():
    """
    Holds the only persistent reference to components and their game objects.
    """

    class Layer():
        def __init__(self):
            # initialize the sprite lists with a dynamic optimized list
            self.sprite_lists = {arcade.SpriteList()}

        def add(self, sprite : arcade.Sprite, sp_hash : bool, sp_hash_csize : int, static : bool) -> None:
            """
            Add a sprite to the layer, given the ideal characteristics of the spritelist it should belong to.
            """
            # does not check to see if the sprite already exists in another sublayer
            
            # instantiate a whole-ass spritelist just to look up a matching one
            # it only gets used if there isnt already a matching one
            # could be better but I figure this will happen at load time so no biggie
            target_sublayer = arcade.SpriteList(use_spatial_hash=sp_hash,
                                                spatial_hash_cell_size=sp_hash_csize,
                                                is_static=static )
            
            # search for matching sprite list
            sublayer = self.sprite_lists.get(spritelist_key(target_sublayer))
            
            # if not found, instantiate one
            if sublayer is None:
                self.sprite_lists[spritelist_key(target_sublayer)] = target_sublayer
            # append sprite to spritelist
                target_sublayer.append(sprite)
            else:
                sublayer.append(sprite)
        
        def remove(self, sprite : arcade.Sprite):
            """
            Remove a sprite from layer.
            """
            for sublayer in self.sprite_lists:
                try:
                    sublayer.remove(sprite)
                except ValueError:
                    continue



    def __init__(self):
        # dict of all used unique IDs
        self.ids = {}
        # list of layers for drawing arcade sprites at different z values
        self.layers = [self.Layer()]

        # list of all dicts that use object ID as key
        self.references = [self.ids]
    
    def create_object(self, name : str) -> str:
        """Add new ID for lookup in this engine's dicts."""
        new_id = get_unique_id(self.ids)
        self.ids[new_id] = name
        return new_id
    
    def destroy_object(self, id):
        """Remove ID from engine's dicts."""
        for dictionary in self.references:
            dictionary.pop(id)
