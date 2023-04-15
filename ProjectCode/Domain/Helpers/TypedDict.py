class TypedDict(dict):
    def __init__(self, key_type, value_type, *args, **kwargs):
        self._key_type = key_type
        self._value_type = value_type
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not isinstance(key, self._key_type):
            raise TypeError(f"Keys must be of type {self._key_type}")
        if not isinstance(value, self._value_type):
            raise TypeError(f"Values must be of type {self._value_type}")
        super().__setitem__(key, value)