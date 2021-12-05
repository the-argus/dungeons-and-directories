from constants.controls import USED_KEYS, USED_CONTROLS

class KeyManager:
    def __init__(self):
        self.keys = {}
        self.modifiers = 0

        self._control_press_handlers = {}
        self._control_release_handlers = {}
        
        for control in USED_CONTROLS:
            for key, modifiers in control.items():
                tmp_control = {key:modifiers}
                self._control_press_handlers[str(tmp_control)] = set()
                self._control_release_handlers[str(tmp_control)] = set()
    
    def on_key_press(self, key, modifiers):
        """called by engine"""
        # update current modifiers
        self.modifiers = modifiers

        # update key state
        if key in USED_KEYS:
            self.keys[key] = True
        
        # call handlers+
        tmp_control = {key : modifiers}
        try:
            for handler in self._control_press_handlers[str(tmp_control)]:
                handler(tmp_control, self)
        except KeyError:
            pass
    
    def on_key_release(self, key, modifiers):
        """called by engine"""
        # update current modifiers
        self.modifiers = modifiers
        if key in USED_KEYS:
            self.keys[key] = False
        
        # call handlers
        tmp_control = {key : modifiers}
        try:
            for handler in self._control_release_handlers[str(tmp_control)]:
                handler(tmp_control, self)
        except KeyError:
            pass
    
    def control_is_pressed(self, control : dict) -> bool:
        """
        used to check whether a single control has been pressed
        (see constants.controls for control format)
        """
        current_modifiers = self.modifiers
        for key, required_modifiers in control.items():
            if self.keys.get(key) and (required_modifiers & current_modifiers == required_modifiers):
                return True
        return False
    
    def add_control_press_handler(self, function, control):
        """adds a function to the set of functions which are executed by the key manager whenever a control is pressed"""
        for key, modifiers in control.items():
                tmp_control = {key:modifiers}
                self._control_press_handlers[str(tmp_control)].add(function)
    
    def add_control_release_handler(self, function, control):
        """adds a function to the set of functions which are executed by the key manager whenever a control is released"""
        for key, modifiers in control.items():
                tmp_control = {key:modifiers}
                self._control_release_handlers[str(tmp_control)].add(function)
    
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