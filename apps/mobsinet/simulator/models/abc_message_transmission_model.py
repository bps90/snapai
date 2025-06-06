from .abc_model import AbcModel
from .nodes.abc_node import AbcNode
from .nodes.packet import Packet


class AbcMessageTransmissionModel(AbcModel):
    def time_to_reach(self,
                      packet: Packet,
                      origin_node: AbcNode,
                      destination_node: AbcNode) -> float:
        """Determines the time that the packet will take to reach the destination node.

        Parameters
        ----------
        packet : Packet
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
