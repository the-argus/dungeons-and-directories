from constants.controls import USED_KEYS

class KeyManager:
    def __init__(self):
        self.keys = {}
        self.modifiers = 0
    
    def on_key_press(self, key, modifiers):
        self.modifiers = modifiers
        if key in USED_KEYS:
            self.keys[key] = True
    
    def on_key_release(self, key, modifiers):
        self.modifiers = modifiers
        if key in USED_KEYS:
            self.keys[key] = False
    
    def control_is_pressed(self, possible_keypresses : dict) -> bool:
        current_modifiers = self.modifiers
        for key, required_modifiers in possible_keypresses.items():
            if self.get(key) and (required_modifiers >= current_modifiers):
                return True
        return False
    
    # passthrough stuff for basic dict functionality
    def __getitem__(self, key):
        return self.keys[key]
    def __setitem__(self, key, value):
        self.keys[key] = value
    def get(self, key, default=None):
        try:
            return self.keys[key]
        except KeyError:
            return default