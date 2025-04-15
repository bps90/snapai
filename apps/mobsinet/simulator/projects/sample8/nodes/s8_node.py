from ....models.nodes.abc_node import AbcNode
from ..messages.s8_message import S8Message
from ....global_vars import Global
from ....tools.color import Color
from ....defaults.nodes.message_timer import MessageTimer
from random import random


class S8Node(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 3

    def check_requirements(self):
        return super().check_requirements()

    def handle_messages(self, inbox):

        if (inbox.single_packet is not None):
            packet = inbox.single_packet
            if (not isinstance(packet.message, S8Message)):
                return
            msg = packet.message
            print('No {} recebendo mensagem {} de Nó {}'.format(
                self.id, msg.color.get_hex(), packet.origin.id))
            # green and yellow messages are forwarded to all neighbors
            if ((msg.color == Color.GREEN or msg.color == Color.YELLOW) and self.node_color != msg.color):
                print('{} broadcasting {}'.format(
                    self.id, msg.color.get_hex()))
                self.broadcast(msg)
            self.set_color(msg.color)
        if (inbox.packet_list is not None):
            for packet in inbox.packet_list:
                if (not isinstance(packet.message, S8Message)):
                    continue
                msg = packet.message

                # green and yellow messages are forwarded to all neighbors
                if ((msg.color == Color.GREEN or msg.color == Color.YELLOW) and self.node_color != msg.color):
                    self.broadcast(msg)
                self.set_color(msg.color)

    def __send_color_message(self, color: Color, to: AbcNode):
        msg = S8Message()
        msg.color = color

        if (Global.is_async_mode):
            if (to is not None):
                self.send(msg, to)
            else:
                self.broadcast(msg)
        else:
            timer = None
            if (to is not None):
                timer = MessageTimer(msg, to)
            else:
                timer = MessageTimer(msg)
            timer.start_relative(random(), self)

    def multicast_red(self):
        self.__send_color_message(Color.RED, None)

    def multicast_blue(self):
        self.__send_color_message(Color.BLUE, None)

    def broadcast_green(self):
        self.__send_color_message(Color.GREEN, None)

    def broadcast_yellow(self):
        self.__send_color_message(Color.YELLOW, None)

    def handle_nack_messages(self, nack_box):
        return super().handle_nack_messages(nack_box)

    def init(self):
        return super().init()

    def on_neighboorhood_change(self):
        return super().on_neighboorhood_change()

    def post_step(self):
        return super().post_step()

    def pre_step(self):
        return super().pre_step()


node = S8Node
