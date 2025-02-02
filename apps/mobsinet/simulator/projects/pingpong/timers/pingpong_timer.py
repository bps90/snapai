from ....models.nodes.abc_timer import AbcTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....projects.pingpong.messages.pingpong_message import PingPongMessage


class PingPongTimer(AbcTimer):
    def __init__(self, msg: 'PingPongMessage', period: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.__msg = msg

    def fire(self):
        self.node.broadcast(self.__msg)

        if (self.period > 0):
            timer = PingPongTimer(self.__msg, self.period)
            timer.start_relative(self.period, self.node)
