from ...models.nodes.abc_timer import AbcTimer
from ...models.nodes.abc_message import AbcMessage
from ...models.nodes.abc_node import AbcNode


class MessageTimer(AbcTimer):
    def __init__(self, msg: 'AbcMessage', receiver: 'AbcNode' = None):
        super().__init__()
        self.msg = msg
        self.receiver = receiver

    def fire(self):
        if (self.receiver is not None):
            self.node.send(self.msg, self.receiver)
        else:
            self.node.broadcast(self.msg)
