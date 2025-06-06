class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0, hex_str: str = None, tuple: tuple = None):
        if hex_str is not None:
            self.set_hex(hex_str)
        elif tuple is not None:
            self.set_tuple(tuple)
        else:
            self.r = r
            self.g = g
            self.b = b

    def get_hex(self):
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'

    def set_hex(self, hex_str: str):
        hex_str = hex_str.lstrip('#')
        self.r = int(hex_str[0:2], 16)
        self.g = int(hex_str[2:4], 16)
        self.b = int(hex_str[4:6], 16)

    def get_tuple(self):
        return (self.r, self.g, self.b)

    def set_tuple(self, tuple):
        self.r = tuple[0]
        self.g = tuple[1]
        self.b = tuple[2]

    def __eq__(self, value):
        if isinstance(value, Color):
            return self.r == value.r and self.g == value.g and self.b == value.b
        elif isinstance(value, str):
            return self.get_hex() == value
        elif isinstance(value, tuple):
            return self.get_tuple() == value
        return False


# Define color constants after the class definition
Color.GREEN = Color(0, 255, 0)
Color.YELLOW = Color(255, 255, 0)
Color.RED = Color(255, 0, 0)
Color.BLUE = Color(0, 0, 255)
Color.PURPLE = Color(128, 0, 128)
