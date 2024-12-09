from ....models.nodes.abc_timer import AbcTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....projects.pingpong.messages.pingpong_message import PingPongMessage


class PingPongTimer(AbcTimer):
    def __init__(self, msg: 'PingPongMessage', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__msg = msg

    def fire(self):
        self.node.broadcast(self.__msg)
