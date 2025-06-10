from ...models.nodes.packet import Packet
from ...models.abc_interference_model import AbcInterferenceModel


class NoInterference(AbcInterferenceModel):

    def is_disturbed(self, packet: Packet) -> bool:
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

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass


model = NoInterference
