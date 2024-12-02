from ....models.nodes.abc_message import AbcMessage

class PingMessage(AbcMessage):
    def __init__(self):
        self.content = "ping"