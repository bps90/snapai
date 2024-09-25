from ...models.abc_message_transmission_model import AbcMessageTransmissionModel
from ...models.nodes.abc_node_implementation import AbcNodeImplementation
from ...models.nodes.abc_packet import AbcPacket
from ...configuration.sim_config import sim_config_env


class ConstantTime(AbcMessageTransmissionModel):

    def __init__(self):
        super().__init__('ConstantTime')

        self.time = sim_config_env.message_transmission_model_parameters[
            'constant_transmission_time']

    def time_to_reach(
            self,
            packet: AbcPacket,
            origin_node: AbcNodeImplementation,
            destination_node: AbcNodeImplementation) -> int:
        """Determines the time that the packet will take to reach the destination node.

        On this model, the time is a constant defined in the configuration or setted directly on the model object.

        Parameters
        ----------
        packet : AbcPacket
            The packet object.
        origin_node : AbcNodeImplementation
            The origin node implementation object.
        destination_node : AbcNodeImplementation
            The destination node implementation object.

        Returns
        -------
        int
            The time that the packet will take to reach the destination node.
        """

        return self.time

    def set_time(self, time: int):
        """Set the time that the packet will take to reach the destination node.

        Parameters
        ----------
        time : int
            The time that the packet will take to reach the destination node.
        """

        self.time = time


model = ConstantTime
