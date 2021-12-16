import arcade

def layer_uid(use_spatial_hash, spatial_hash_cell_size):
    """
    create a number that will always be unique for a spritelist with
    the given properties.
    """
    uid = spatial_hash_cell_size << use_spatial_hash
    return uid

class Layer:
    """
class meant to hold a set of sprite lists with different properties
a set of these will be initialized in the engine and then drawn in
order.
"""
    def __init__(self):
        self.sublayers = {}
        self._visible = True
    
    def add_sprite(self, sprite, use_spatial_hash, spatial_hash_cell_size):
        """
        Add a sprite to this layer with the given draw properties
        Assumes a sprite will never be added in duplicate to
        multiple sublayers.
        """
        assert isinstance(sprite, arcade.Sprite)

        uid = layer_uid(use_spatial_hash, spatial_hash_cell_size)
        if not self.sublayers.get(uid, False):
            self.sublayers[uid] = arcade.SpriteList(use_spatial_hash=use_spatial_hash,
                                                    spatial_hash_cell_size=spatial_hash_cell_size)
        self.sublayers[uid].append(sprite)
    
    def remove_sprite(self, sprite):
        """Removes the first instance found of a sprite in sublayers."""
        for uid, spritelist in self.sublayers.items():
            try:
                spritelist.remove(sprite)
                # cleaup
                if len(spritelist) == 0:
                    self.sublayers.pop(uid)
                return True
            except ValueError:
                # sprite not found in sublayer
                pass
        return False
    
    def draw(self, filter=arcade.gl.NEAREST, pixelated=True, blend_function=None):
        for uid, spritelist in self.sublayers.items():
            spritelist.draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
    
    def update(self):
        for uid, spritelist in self.sublayers.items():
            spritelist.update()
    
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, value):
        if isinstance(value, bool):
            for uid, spritelist in self.sublayers.items():
                spritelist.visible = value
            self._visible = value