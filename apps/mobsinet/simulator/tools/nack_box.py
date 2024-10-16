# GENERATED WITH HELP FROM CHATGPT

from .inbox import Inbox
from ..models.nodes.abc_packet import AbcPacket


class NackBox(Inbox):
    """
    O equivalente ao Inbox para mensagens que não chegaram ao destino.

    Sempre que uma mensagem é descartada, o remetente é informado através
    do método handleNAckMessages().

    Este recurso precisa ser ativado na configuração do projeto:
    defina generateNAckMessages como True. Se um nó remetente não precisa
    ser informado sobre mensagens descartadas, esse recurso pode ser desativado
    para economizar poder computacional.
    """

    def __init__(self, packets: 'AbcPacket' | list['AbcPacket'] = None):
        """
        Construtor para criar um NackBox contendo uma lista de pacotes ou um único pacote.

        Parameters
        ----------
        packets : AbcPacket or list['AbcPacket']
            Pode ser um único pacote ou uma lista de pacotes.

        """
        super().__init__(packets)

    def reset_for_packet(self, packet):
        """
        Método para redefinir o NackBox para conter um único pacote.

        Parameters
        ----------
        packet : AbcPacket
            O pacote a ser incluído neste NackBox.

        Returns
        -------
        NackBox
            Este objeto NackBox com o pacote incluído.
        """
        super().reset_for_packet(packet)
        return self
