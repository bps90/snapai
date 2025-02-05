from ....models.nodes.abc_node import AbcNode
from ..messages.pingpong_message import PingPongMessage
from ..timers.pingpong_timer import PingPongTimer
from ..timers.init_pingpong_timer import InitPingPongTimer
from ....tools.color import Color
from random import randint
from ....global_vars import Global
from ....network_simulator import simulation
from ....configuration.sim_config import config


class PingPongNode(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pingpong_inited = False
        self.__local_r: int = 0
        self.__local_g: int = 0
        self.__local_b: int = 0
        self.size = 10
        if (len(simulation.nodes()) == 0):
            init_pingpong_timer = InitPingPongTimer()
            init_pingpong_timer.start_relative(1, self)

    def init_pingpong(self):
        if (not self.pingpong_inited):
            self.pingpong_inited = True
            message = PingPongMessage()
            message.set_r(randint(0, 255))
            message.set_g(randint(0, 255))
            message.set_b(randint(0, 255))

            timer = PingPongTimer(message, 10)
            timer.start_relative(1, self)

    def handle_messages(self, inbox):
        received_from = []

        for packet in inbox.packet_list:
            message = packet.message
            if (isinstance(message, PingPongMessage) and packet.origin not in received_from):
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

                received_from.append(packet.origin)

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
