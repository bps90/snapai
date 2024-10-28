from .abc_model import AbcModel
from .nodes.abc_node_implementation import AbcNodeImplementation
from .nodes.packet import Packet


class AbcMessageTransmissionModel(AbcModel):
    def time_to_reach(self,
                      packet: Packet,
                      origin_node: AbcNodeImplementation,
                      destination_node: AbcNodeImplementation) -> int:
        """Determines the time that the packet will take to reach the destination node.

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
        pass
