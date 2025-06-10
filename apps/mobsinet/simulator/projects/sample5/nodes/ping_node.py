from ....models.nodes.abc_node import AbcNode
from ..messages.pong_message import PongMessage
from ..messages.ping_message import PingMessage
from ....global_vars import Global


class PingNode(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 3

    def handle_messages(self, inbox):
        # Return a pong message
        message = PongMessage()

        for packet in inbox.packet_list:
            if (not isinstance(packet.message, PingMessage)):
                continue

            self.send(message, packet.origin)

    def handle_nack_messages(self, nack_box):
        return super().handle_nack_messages(nack_box)

    def check_requirements(self):
        pass

    def init(self):
        pass

    def on_neighboorhood_change(self):
        pass

    def pre_step(self):
        pass

    def post_step(self):
        if (Global.current_time == 1):
            message = PingMessage()
            self.broadcast(message)


node = PingNode
