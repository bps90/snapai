from ....models.nodes.abc_node import AbcNode
from ..messages.s8_message import S8Message
from ....global_vars import Global
from ....tools.color import Color, GREEN, YELLOW, RED, BLUE
from ....defaults.nodes.message_timer import MessageTimer
from random import random
from typing import Optional


class S8Node(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 3

    def handle_messages(self, inbox):

        if (inbox.single_packet is not None):
            packet = inbox.single_packet
            if (not isinstance(packet.message, S8Message)):
                return
            msg = packet.message
            print('No {} recebendo mensagem {} de Nó {}'.format(
                self.id, msg.color.get_hex(), packet.origin.id))
            # green and yellow messages are forwarded to all neighbors
            if ((msg.color == GREEN or msg.color == YELLOW) and self.node_color != msg.color):
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
                if ((msg.color == GREEN or msg.color == YELLOW) and self.node_color != msg.color):
                    self.broadcast(msg)
                self.set_color(msg.color)

    def __send_color_message(self, color: Color, to: Optional[AbcNode]):
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
        self.__send_color_message(RED, None)

    def multicast_blue(self):
        self.__send_color_message(BLUE, None)

    def broadcast_green(self):
        self.__send_color_message(GREEN, None)

    def broadcast_yellow(self):
        self.__send_color_message(YELLOW, None)

    def handle_nack_messages(self, nack_box):
        return super().handle_nack_messages(nack_box)

    def check_requirements(self):
        pass

    def init(self):
        pass

    def on_neighboorhood_change(self):
        pass

    def post_step(self):
        pass

    def pre_step(self):
        pass


node = S8Node
