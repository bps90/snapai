from ....models.nodes.abc_message import AbcMessage
from ....tools.color import Color


class S8Message(AbcMessage):
    def __init__(self):
        # TODO: verificar se o método clone funciona se tiver outras variáveis

        self.color: Color = None
