from ....models.nodes.abc_timer import AbcTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..nodes.pingpong_node import PingPongNode


class InitPingPongTimer(AbcTimer):

    def fire(self):
        if (self.node is None):
            raise Exception("Node is None")
        if (not isinstance(self.node, PingPongNode)):
            raise Exception("Node is not PingPongNode")
        self.node.init_pingpong()
