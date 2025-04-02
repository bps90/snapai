from ....models.nodes.abc_message import AbcMessage


class PingPongMessage(AbcMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__r: int = 0
        self.__g: int = 0
        self.__b: int = 0

    def get_r(self):
        return self.__r

    def get_g(self):
        return self.__g

    def get_b(self):
        return self.__b

    def set_r(self, r: int):
        self.__r = r
        self.content = f"Change color to #{self.__r:02x}{self.__g:02x}{self.__b:02x}"

    def set_g(self, g: int):
        self.__g = g
        self.content = f"Change color to #{self.__r:02x}{self.__g:02x}{self.__b:02x}"

    def set_b(self, b: int):
        self.__b = b
        self.content = f"Change color to #{self.__r:02x}{self.__g:02x}{self.__b:02x}"
