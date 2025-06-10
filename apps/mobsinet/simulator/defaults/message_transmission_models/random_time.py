import random
from ...models.abc_message_transmission_model import AbcMessageTransmissionModel
from ...models.nodes.abc_node import AbcNode
from ...models.nodes.packet import Packet
from ...configuration.sim_config import SimulationConfig
from typing import TypedDict


class RandomTimeParameters(TypedDict):
    min_time: float
    max_time: float


class RandomTime(AbcMessageTransmissionModel):
    def __init__(self, parameters: RandomTimeParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

    def check_parameters(self, parameters):
        if ('min_time' not in parameters or
                (not isinstance(parameters['min_time'], float) and not isinstance(parameters['min_time'], int)) or
                parameters['min_time'] < 0):
            return False

        if ('max_time' not in parameters or
                (not isinstance(parameters['max_time'], float) and not isinstance(parameters['max_time'], int)) or
                parameters['max_time'] < 0 or
                parameters['max_time'] < parameters['min_time']):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: RandomTimeParameters = parameters
        self.min_time: float = parsed_parameters['min_time']
        self.max_time: float = parsed_parameters['max_time']

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
        float
            The time that the packet will take to reach the destination node.
        """

        return random.uniform(self.min_time, self.max_time)

    def set_interval(self,
                     min_time: float,
                     max_time: float):
        """Set the min and max time that the packet will take to reach the destination node.

        Parameters
        ----------
        min_time : float (optional)
            The min time that the packet will take to reach the destination node.
            By default, the min time is defined in the configuration.
        max_time : float (optional)
            The max time that the packet will take to reach the destination node.
            By default, the max time is defined in the configuration.
        """

        self.min_time = min_time
        self.max_time = max_time


model = RandomTime
