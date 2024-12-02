from ....models.nodes.abc_node import AbcNode
from ..messages.pong_message import PongMessage
from ..messages.ping_message import PingMessage

class PingNode(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def check_requirements(self):
        return super().check_requirements()
    
    def handle_messages(self, inbox):
        # Return a pong message
        message = PongMessage()
        
        for packet in inbox.packet_list:
            self.send(message, packet.origin)
        
    
    def init(self):
        return super().init()
    
    def on_neighboorhood_change(self):
        return super().on_neighboorhood_change()
    
    def post_step(self):
        message = PingMessage()
        self.broadcast(message)
    
    def pre_step(self):
        return super().pre_step()
    
node = PingNode