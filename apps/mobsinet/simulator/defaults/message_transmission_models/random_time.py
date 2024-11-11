import random
from ...models.abc_message_transmission_model import AbcMessageTransmissionModel
from ...models.nodes.abc_node import AbcNode
from ...models.nodes.packet import Packet
from ...configuration.sim_config import config

parameters = config.message_transmission_model_parameters


class RandomTime(AbcMessageTransmissionModel):
    def __init__(self):
        super().__init__('RandomTime')

        self.min_time = parameters['random_transmission_min_time']
        self.max_time = parameters['random_transmission_max_time']

    def time_to_reach(self,
                      packet: Packet,
                      origin_node: AbcNode,
                      destination_node: AbcNode):
        """Determines the time that the packet will take to reach the destination node.

        On this model, the time is a random number between 
        the min and max time defined in the configuration 
        or setted directly on the model object.

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
        int
            The time that the packet will take to reach the destination node.
        """

        return random.randint(self.min_time, self.max_time)

    def set_interval(self,
                     min_time: int = parameters['random_transmission_min_time'],
                     max_time: int = parameters['random_transmission_max_time']):
        """Set the min and max time that the packet will take to reach the destination node.

        Parameters
        ----------
        min_time : int (optional)
            The min time that the packet will take to reach the destination node.
            By default, the min time is defined in the configuration.
        max_time : int (optional)
            The max time that the packet will take to reach the destination node.
            By default, the max time is defined in the configuration.
        """

        self.min_time = min_time
        self.max_time = max_time


model = RandomTime
