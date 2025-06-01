# GENERATED WITH HELP FROM CHATGPT

from .inbox import Inbox
from ..models.nodes.packet import Packet
from typing import Union


class NackBox(Inbox):
   

    def __init__(self, packets: Union['Packet', list['Packet']] = None):
        """
        Construtor para criar um NackBox contendo uma lista de pacotes ou um único pacote.

        Parameters
        ----------
        packets : Packet or list['Packet']
            Pode ser um único pacote ou uma lista de pacotes.

        """
        super().__init__(packets)

    def reset_for_packet(self, packet: 'Packet'):
        """
        Método para redefinir o NackBox para conter um único pacote.

        Parameters
        ----------
        packet : Packet
            O pacote a ser incluído neste NackBox.

        Returns
        -------
        NackBox
            Este objeto NackBox com o pacote incluído.
        """
        super().reset_for_packet(packet)
        return self
