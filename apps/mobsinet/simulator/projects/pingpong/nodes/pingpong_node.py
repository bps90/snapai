from ....models.nodes.abc_node import AbcNode
from ..messages.pingpong_message import PingPongMessage
from ..timers.pingpong_timer import PingPongTimer
from ....tools.color import Color
from random import randint


class PingPongNode(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__local_r: int = 0
        self.__local_g: int = 0
        self.__local_b: int = 0

    def handle_messages(self, inbox):
        for packet in inbox.packet_list:
            message = packet.message
            if (isinstance(message, PingPongMessage)):
                self.__local_r = message.get_r()
                self.__local_g = message.get_g()
                self.__local_b = message.get_b()

                self.set_color(
                    Color(self.__local_r, self.__local_g, self.__local_b))

                message.set_r(randint(0, 255))
                message.set_g(randint(0, 255))
                message.set_b(randint(0, 255))

                timer = PingPongTimer(message)
                timer.start_relative(1, self)

    def check_requirements(self):
        return super().check_requirements()

    def init(self):
        return super().init()

    def on_neighboorhood_change(self):
        return super().on_neighboorhood_change()

    def post_step(self):
        return super().post_step()

    def pre_step(self):
        return super().pre_step()


node = PingPongNode
