from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from ...tools.inbox_packet_buffer import InboxPacketBuffer
from .packet import Packet
from .abc_message import AbcMessage
from ...tools.packet_type import PacketType
from ...tools.nack_box import NackBox
from ...global_vars import Global
from ...network_simulator import simulation

if TYPE_CHECKING:
    from .abc_timer import AbcTimer
    from ...tools.position import Position
    from ..abc_mobility_model import AbcMobilityModel
    from ..abc_connectivity_model import AbcConnectivityModel
    from ..abc_interference_model import AbcInterferenceModel
    from ..abc_reliability_model import AbcReliabilityModel
    from ...tools.inbox import Inbox


class AbcNode(ABC):
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
        self.timersToHandle: list['AbcTimer'] = []
        self.neighboorhood_changed: bool = False
        self.packet_buffer = InboxPacketBuffer()
        self.nack_buffer_odd: list['Packet'] = []
        self.nack_buffer_even: list['Packet'] = []
        self.nack_box: 'NackBox' | None = None
        self.inbox: 'Inbox' | None = None
        self.intensity: float = 1.0
        # self.outgoing_connections: list['EdgeImplementation'] = []

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
        self.node_position_updated()

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
    
    def equals(self, object: object | 'AbcNode'):
        if (object == None): return False
        elif (isinstance(object, AbcNode)):
            return self.id == object.id
        return False
    
    def set_radio_intensity(self, intensity: float):
        if (intensity < 0):
            self.intensity = 0
        elif (intensity > 1):
            self.intensity = 1
        else:
            self.intensity = intensity
            
    def get_radio_intensity(self):
        return self.intensity

    def send(self, message: 'AbcMessage', destination: 'AbcNode', intensity: float = None):
        intensity = intensity if intensity != None else self.intensity
        
        has_edge = simulation.has_edge(self, destination)
        
        packet = self.__sendMessage(message, has_edge, self, destination, intensity)
        
        simulation.packets_in_the_air.add(packet)
        
    def __sendMessage(self, msg: 'AbcMessage', has_edge: bool, sender: 'AbcNode', destination: 'AbcNode', intensity: float):
        return self.__synchronousSending(msg, has_edge, sender, destination, intensity)

    def __synchronousSending(self, msg: 'AbcMessage', has_edge: bool, sender: 'AbcNode', destination: 'AbcNode', intensity: float):
        if (not Global.is_running): return
        
        cloned_message = msg.clone()
        
        if (cloned_message == None): raise Exception("Cloned message is None")

        packet = Packet(cloned_message)
        transmission_time = Global.message_transmission_model.time_to_reach(packet, sender, destination)
        
        packet.arriving_time = Global.currentTime + transmission_time
        packet.sending_time = Global.currentTime
        packet.origin = sender
        packet.destination = destination
        packet.intensity = intensity
        packet.type = PacketType['UNICAST']
        
        if (has_edge):
            packet.positive_delivery = self.reliability_model.reaches_destination(packet)
            simulation.graph.edges[sender, destination]['number_of_packets'] += 1
        else:
            packet.positive_delivery = False

        destination.packet_buffer.add_packet(packet)
    
        Global.number_of_messages_in_this_round += 1
        
        return packet

    def set_coordinates(self, x: int, y: int, z: int):
        return self.position.set_coordinates(x, y, z)

    def node_position_updated(self):
        """Action to be performed when the node's position is updated.

        Can be implemented by subclasses.
        """
        pass

    def add_timer(self, timer: 'AbcTimer'):
        """Adds a timer to the node.

        Parameters
        ----------
        timer : AbcTimer
            The timer object.
        """

        self.timers.append(timer)

    @abstractmethod
    def init(self): 
        pass

    @abstractmethod
    def pre_step(self):
        """Action to be performed before the node performs a step.

        Can be implemented by subclasses.
        """
        pass

    @abstractmethod
    def post_step(self):
        """Action to be performed at the end of the node step.

        Can be implemented by subclasses.
        """
        pass

    @abstractmethod
    def on_neighboorhood_change(self):
        """Action to be performed when the node's neighboorhood changes.

        Can be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def check_requirements(self):
        pass

    def handle_nack_messages(self, nack_box: 'NackBox'):
        """The user can override this method to handle nack messages.

        Parameters
        ----------
        nack_box : NackBox
            The nack box object.
        """
        pass

    @abstractmethod
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

        for timer in self.timers:
            if (timer.fire_time <= Global.current_time):
                self.timers.remove(timer)
                self.timersToHandle.append(timer)

        # sort timersToHandle
        self.timersToHandle.sort(key=lambda timer: timer.fire_time)

        for timer in self.timersToHandle:
            timer.fire()

        if (self.nack_box is None):
            self.nack_box = NackBox(self.nack_buffer_even if Global.is_even_round else self.nack_buffer_odd)
        else:
            self.nack_box.reset_for_list(self.nack_buffer_even if Global.is_even_round else self.nack_buffer_odd)


        self.handle_nack_messages(self.nack_box) 
        self.inbox = self.packet_buffer.get_inbox()
        self.handle_messages(self.inbox)

        self.post_step()

        self.inbox.free_packets()
        self.nack_box.free_packets()

    def add_nack_packet(self, packet: 'Packet'):
        # Verifica se o tipo de pacote é UNICAST
        if packet.type != PacketType['UNICAST']:
            return  # Somente reconhece pacotes UNICAST

        # Adiciona o pacote ao buffer
        if Global.is_even_round:
            self.nack_buffer_odd.append(packet)
        else:
            self.nack_buffer_even.append(packet)
