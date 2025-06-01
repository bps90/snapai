from ....models.nodes.abc_message import AbcMessage


class PingMessage(AbcMessage):
    def __init__(self):
        # TODO: verificar se o método clone funciona se tiver outras variáveis
        # self.outra = "outra"
        self.content = "ping"
