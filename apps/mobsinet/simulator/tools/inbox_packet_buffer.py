# GENERATED WITH HELP FROM CHATGPT

from ..network_simulator import simulation
from ..models.nodes.abc_packet import AbcPacket
from .inbox import Inbox


class InboxPacketBuffer:
    def __init__(self, keep_finger=False):
        # Lista de pacotes que chegam neste round
        self.arriving_packets: list['AbcPacket'] = []
        self.buffer: list['AbcPacket'] = []
        self.inbox: 'Inbox' = None
        self.keep_finger = keep_finger

    def add_packet(self, p: 'AbcPacket'):
        """Adiciona um pacote à lista."""
        self.buffer.append(p)

    def remove_packet(self, p: 'AbcPacket'):
        """Remove um pacote da lista."""
        try:
            self.buffer.remove(p)
        except ValueError:
            pass  # Se o pacote não estiver na lista, ignore

    def update_message_buffer(self):
        """Atualiza o buffer de mensagens, processando pacotes que chegaram."""
        self.arriving_packets.clear()

        # Criando uma cópia para evitar modificação da lista durante iteração
        for p in self.buffer[:]:
            if p.arriving_time <= simulation.global_time:

                simulation.packets_in_the_air.remove(p)

                self.buffer.remove(p)

                if p.positive_delivery:
                    self.arriving_packets.append(p)
                else:
                    # if sim_config_env.generate_nack_messages:
                    # Retorna o pacote ao remetente
                    p.origin.add_nack_packet(p)
                    # else:
                    #     AbcPacket.free(p)

    def waiting_packets(self) -> int:
        """Retorna o número de pacotes que estão esperando."""
        return len(self.arriving_packets)

    def get_inbox(self) -> 'Inbox':
        """Obtém a Inbox com os pacotes que chegaram."""
        self.arriving_packets.sort()
        if self.inbox is None:
            self.inbox = Inbox(self.arriving_packets)
        else:
            self.inbox.reset_for_list(self.arriving_packets)
        return self.inbox
