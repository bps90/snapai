class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def get_hex(self):
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'

    def set_hex(self, hex_str: str):
        self.r = int(hex_str[1:3], 16)
        self.g = int(hex_str[3:5], 16)
        self.b = int(hex_str[5:7], 16)

    def get_tuple(self):
        return (self.r, self.g, self.b)

    def set_tuple(self, tuple):
        self.r = tuple[0]
        self.g = tuple[1]
        self.b = tuple[2]
