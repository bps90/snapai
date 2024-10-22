import threading
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .abc_message import AbcMessage

if TYPE_CHECKING:
    from .abc_node_implementation import AbcNodeImplementation


class AbcPacket(ABC):
    issued_packets = set()  # Usamos um conjunto para armazenar os pacotes emitidos
    free_packets = []  # Pilha para armazenar pacotes livres
    num_packets_on_the_fly = 0  # Contador de pacotes em uso
    lock = threading.Lock()  # Lock para controle de concorrência

    def __init__(self,
                 message: 'AbcMessage',
                 origin: 'AbcNodeImplementation',
                 destination: 'AbcNodeImplementation',
                 type: str):
        self.message = message
        self.origin = origin
        self.destination = destination
        self.type = type
        self.positive_delivery: bool = True
        self.arriving_time: int = 0
        self.sending_time: int = 0

    def set_message(self, message: 'AbcMessage'):
        self.message = message

    def denyDelivery(self):
        """Deny the delivery of the packet."""

        self.positive_delivery = False

    @abstractmethod
    def clone(self):
        """Create a copy of the object.

        Returns
        -------
        AbcPacket
            A copy of the object.
        """
        # TODO: implement
        pass

    @staticmethod
    def free(packet: 'AbcPacket'):
        """This method marks this packet as unused. 
        This means that it adds itself to the packet 
        pool and can thus be recycled by the 
        fabricatePacket-method.

        Parameters
        ----------
        packet : AbcPacket
            The packet to free.
        """
        # GENERATED WITH HELP FROM CHATGPT

        with AbcPacket.lock:
            # Remove o pacote da lista de pacotes emitidos
            if packet not in AbcPacket.issued_packets:
                print(
                    "Erro na fábrica de pacotes. Por favor, relate este erro se você vir esta mensagem.")
            else:
                AbcPacket.issued_packets.remove(packet)

            # Reduz o contador de pacotes em uso
            AbcPacket.num_packets_on_the_fly -= 1

            # Limpa as informações do pacote
            packet.destination = None
            packet.origin = None
            packet.message = None

            # Adiciona o pacote à pilha de pacotes livres
            AbcPacket.free_packets.append(packet)
