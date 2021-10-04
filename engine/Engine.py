import arcade
from numbers import Number
from tools import spritelist_key, get_unique_id, get_default_args
from CONSTANTS import LAYERS

class Engine():
    """
    Holds the only persistent reference to components and their game objects.
    """
    class Buffer(dict):
        def __init__(self):
            super().__init__(self)
            self.changed = True
        def setitem(self, key, value):
            super().__setitem__(self, key, value)
            self.changed = True
            

    class Layer():
        def __init__(self):
            # initialize the sprite lists with a dynamic optimized list
            init_list = arcade.SpriteList()
            init_list.initialize()
            self.sprite_lists = {init_list}

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
                target_sublayer.initialize()
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
        self.layers = [self.Layer() for i in range(LAYERS)]
        
        # sprite info
        self.sprite_pos = self.Buffer()
        self.sprite_size = self.Buffer()
        self.sprite_angle = self.Buffer()
        self.sprite_color = self.Buffer()
        self.sprite_texture = self.Buffer()

        # list of all dicts that use object ID as key
        self.references = [self.ids]
    
    def create_object(self, name : str, coords = (), **kwargs) -> str:
        """Add new ID for lookup in this engine's dicts."""
        new_id = get_unique_id(self.ids)
        self.ids[new_id] = name
        
        # assign object coordinates if provided
        if len(coords) == 2 and isinstance(coords[0], Number):
            self.coords[new_id] = coords
        
        sprite = kwargs.get('sprite')
        if sprite is not None:
            self.add_sprite(new_id, sprite, **kwargs)


        return new_id
    
    def drawall(self):
        if any(
            self.sprite_pos.changed,
            self.sprite_size.changed,
            self.sprite_angle.changed,
            self.sprite_color.changed,
            self.sprite_texture.changed
        ):
            # first update 

            for layer in self.layers:
                for id, spritelist in layer.sprite_lists.items():
                    spritelist._write_sprite_buffers_to_gpu()
    
    def destroy_object(self, id):
        """Remove ID from engine's dicts."""
        for dictionary in self.references:
            dictionary.pop(id)
    
    def add_sprite(self, object_id : str, sprite: arcade.Sprite, z_value = 0, **kwargs):
        if z_value >= LAYERS or z_value < 0:
            raise Exception("z_value not within layers.")
        if not isinstance(z_value, int):
            raise Exception("z_value must be an integer.")
        self.sprites[object_id] = sprite

        # the default values for arcade.SpriteList:
        default = get_default_args(arcade.SpriteList.__init__)

        # get kwargs if they exist, otherwise use default spritelist values
        use_spatial_hash = kwargs.get('use_spatial_hash', default.get('use_spatial_hash'))
        spatial_hash_cell_size = kwargs.get('spatial_hash_cell_size', default.get('spatial_hash_cell_size'))
        is_static = kwargs.get('is_static', default.get('is_static'))

        # add sprite to layer's correct sublayer
        self.layers[z_value].add(sprite, use_spatial_hash, spatial_hash_cell_size, is_static)
