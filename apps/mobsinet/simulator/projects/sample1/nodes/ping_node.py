from ....models.nodes.abc_node import AbcNode
from ..messages.pong_message import PongMessage
from ..messages.ping_message import PingMessage
from ....global_vars import Global


class PingNode(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 3

    def check_requirements(self):
        return super().check_requirements()

    def handle_messages(self, inbox):
        # Return a pong message
        message = PongMessage()

        for packet in inbox.packet_list:
            if (not isinstance(packet.message, PingMessage)):
                continue

            self.send(message, packet.origin)

    def handle_nack_messages(self, nack_box):
        return super().handle_nack_messages(nack_box)

    def init(self):
        return super().init()

    def on_neighboorhood_change(self):
        return super().on_neighboorhood_change()

    def post_step(self):
        if (Global.current_time == 1):
            message = PingMessage()
            self.broadcast(message)

    def pre_step(self):
        return super().pre_step()


node = PingNode
