from ...models.abc_message_transmission_model import AbcMessageTransmissionModel
from ...models.nodes.abc_node import AbcNode
from ...models.nodes.packet import Packet
from ...configuration.sim_config import config


class ConstantTime(AbcMessageTransmissionModel):

    def __init__(self):
        super().__init__('ConstantTime')

        self.time = config.message_transmission_model_parameters[
            'constant_transmission_time']

    def time_to_reach(
            self,
            packet: Packet,
            origin_node: AbcNode,
            destination_node: AbcNode) -> float:
        """Determines the time that the packet will take to reach the destination node.

        On this model, the time is a constant defined in the configuration or setted directly on the model object.

        Parameters
        ----------
        packet : AbcPacket
            The packet object.
        origin_node : AbcNode
            The origin node object.
        destination_node : AbcNode
            The destination node object.

        Returns
        -------
        float
            The time that the packet will take to reach the destination node.
        """

        return self.time

    def set_time(self, time: float):
        """Set the time that the packet will take to reach the destination node.

        Parameters
        ----------
        time : int
            The time that the packet will take to reach the destination node.
        """

        self.time = float


model = ConstantTime
