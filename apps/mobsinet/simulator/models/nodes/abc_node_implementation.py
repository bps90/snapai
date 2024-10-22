from typing import TYPE_CHECKING
from abc import ABC
from ...network_simulator import simulation
from ...tools.inbox_packet_buffer import InboxPacketBuffer
from .abc_packet import AbcPacket
from ...tools.packet_type import PacketType
from ...tools.nack_box import NackBox

if TYPE_CHECKING:
    from .abc_timer import AbcTimer
    from ...tools.position import Position
    from ..abc_mobility_model import AbcMobilityModel
    from ..abc_connectivity_model import AbcConnectivityModel
    from ..abc_interference_model import AbcInterferenceModel
    from ..abc_reliability_model import AbcReliabilityModel
    from ...tools.inbox import Inbox


class AbcNodeImplementation(ABC):

    timersToHandle: list['AbcTimer'] = []

    def __init__(
            self,
            id: int,
            position: 'Position' = None,
            mobility_model: 'AbcMobilityModel' = None,
            connectivity_model: 'AbcConnectivityModel' = None,
            interference_model: 'AbcInterferenceModel' = None,
            reliability_model: 'AbcReliabilityModel' = None):
        self.id = id
        self.position: Position = position
        self.mobility_model: AbcMobilityModel = mobility_model
        self.connectivity_model: AbcConnectivityModel = connectivity_model
        self.interference_model: AbcInterferenceModel = interference_model
        self.reliability_model: AbcReliabilityModel = reliability_model

        self.timers: list[AbcTimer] = []
        self.neighboorhood_changed: bool = False
        self.packet_buffer = InboxPacketBuffer()
        self.nack_buffer: list['AbcPacket'] = []
        self.nack_box: 'NackBox' | None = None
        self.inbox: 'Inbox' | None = None

    def __str__(self):
        return f"""
ID: {self.id}
Position: {self.position}
Mobility Model: {self.mobility_model.name}
Connectivity Model: {self.connectivity_model.name}
Interference Model: {self.interference_model.name}
Reliability Model: {self.reliability_model.name}
"""

    def __repr__(self) -> str:
        return self.__str__()

    def set_position(self, position: 'Position'):
        self.position = position

    def set_mobility_model(self, mobility_model: 'AbcMobilityModel'):
        self.mobility_model = mobility_model

    def set_connectivity_model(self, connectivity_model: 'AbcConnectivityModel'):
        self.connectivity_model = connectivity_model

    def set_interference_model(self, interference_model: 'AbcInterferenceModel'):
        self.interference_model = interference_model

    def set_reliability_model(self, reliability_model: 'AbcReliabilityModel'):
        self.reliability_model = reliability_model

    def get_coordinates(self):
        return self.position.get_coordinates()

    def set_coordinates(self, x: int, y: int, z: int):
        return self.position.set_coordinates(x, y, z)

    def add_timer(self, timer: 'AbcTimer'):
        """Adds a timer to the node.

        Parameters
        ----------
        timer : AbcTimer
            The timer object.
        """

        self.timers.append(timer)

    def pre_step(self):
        """Action to be performed before the node performs a step.

        Can be implemented by subclasses.
        """
        pass

    def post_step(self):
        """Action to be performed at the end of the node step.

        Can be implemented by subclasses.
        """
        pass

    def on_neighboorhood_change(self):
        """Action to be performed when the node's neighboorhood changes.

        Can be implemented by subclasses.
        """
        pass

    def handle_nack_messages(self, nack_box: 'NackBox'):
        """The user can override this method to handle nack messages.

        Parameters
        ----------
        nack_box : NackBox
            The nack box object.
        """
        pass

    def handle_messages(self, inbox: 'Inbox'):
        """This method is invoked after all the Messages are received. 
        Overwrite it to specify what to do  with incoming messages.

        Parameters
        ----------
        inbox : Inbox
            The inbox object.
        """
        pass

    def step(self):
        """Performs a step for the node.

        Should not be overridden.
        """

        self.packet_buffer.update_message_buffer()

        self.pre_step()

        if self.neighboorhood_changed:
            self.on_neighboorhood_change()

        self.timersToHandle.clear()

        if (len(self.timers) > 0):
            for timer in self.timers:
                if (timer.fire_time <= simulation.global_time):
                    self.timers.remove(timer)
                    self.timersToHandle.append(timer)

            # sort timersToHandle
            self.timersToHandle.sort(key=lambda timer: timer.fire_time)

            for timer in self.timersToHandle:
                timer.fire()

        if (self.nack_box is None):
            self.nack_box = NackBox(self.nack_buffer)
        else:
            self.nack_box.reset_for_list(self.nack_buffer)

        self.handle_nack_messages(self.nack_box)

        self.inbox = self.packet_buffer.get_inbox()
        self.handle_messages(self.inbox)

        self.post_step()

        self.inbox.free_packets()
        self.nack_box.free_packets()

    def add_nack_packet(self, packet: 'AbcPacket'):
        # Verifica se o tipo de pacote é UNICAST
        if packet.type != PacketType['UNICAST']:
            return  # Somente reconhece pacotes UNICAST

        # Adiciona o pacote ao buffer
        self.nack_buffer.append(packet)
