from abc import abstractmethod

from apps.mobsinet.simulator.models.nodes.abc_packet import AbcPacket
from .abc_model import AbcModel


class AbcReliabilityModel(AbcModel):

    @abstractmethod
    def reaches_destination(self, packet: AbcPacket) -> bool:
        pass
