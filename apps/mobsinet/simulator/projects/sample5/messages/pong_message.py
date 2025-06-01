from ....models.nodes.abc_message import AbcMessage

class PongMessage(AbcMessage):
    def __init__(self):
        self.content = "pong"