from apps.mobsinet.simulator.models.nodes.abc_packet import AbcPacket
from ...models.abc_interference_model import AbcInterferenceModel


class NoInterference(AbcInterferenceModel):
    def __init__(self):
        super().__init__('NoInterference')

    def is_disturbed(self, packet: AbcPacket) -> bool:
        """Checks if the interference model dirtubed the packet.

        The packet will not be disturbed in this model.

        Parameters
        ----------
        packet : AbcPacket
            The packet to check.

        Returns
        -------
        bool
            False everywhere.
        """

        return False


model = NoInterference
