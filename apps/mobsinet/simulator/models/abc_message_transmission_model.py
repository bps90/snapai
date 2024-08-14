from apps.mobsinet.simulator.models.abc_model import AbcModel
from apps.mobsinet.simulator.models.nodes.abc_node_implementation import AbcNodeImplementation
from apps.mobsinet.simulator.models.nodes.abc_packet import AbcPacket


class AbcMessageTransmissionModel(AbcModel):
    def time_to_reach(self,
                      packet: AbcPacket,
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
