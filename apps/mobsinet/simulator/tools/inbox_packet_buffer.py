# GENERATED WITH HELP FROM CHATGPT

from ..network_simulator import simulation
from ..models.nodes.packet import Packet
from .inbox import Inbox
from ..global_vars import Global
from typing import TYPE_CHECKING

if (TYPE_CHECKING):
    from ..models.nodes.abc_node import AbcNode


class InboxPacketBuffer:
    def __init__(self):
        # Lista de pacotes que chegam neste round
        self.arriving_packets: list['Packet'] = []
        self.buffer: list['Packet'] = []
        self.inbox: 'Inbox' = None

    def add_packet(self, p: 'Packet'):
        """Adiciona um pacote à lista."""
        self.buffer.append(p)

    def remove_packet(self, p: 'Packet'):
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
            if p.arriving_time <= Global.current_time:

                simulation.packets_in_the_air.remove(p)

                self.buffer.remove(p)

                # if p.edge:
                #     p.edge.remove_message_for_this_edge(p.message)

                if p.positive_delivery:
                    self.arriving_packets.append(p)
                    Global.round_logs.append(
                        f"Packet \"{p.message.content}\" ({p.origin.id}->{p.destination.id}) arrived"
                    )
                else:
                    # if sim_config_env.generate_nack_messages:
                    # Retorna o pacote ao remetente
                    p.origin.add_nack_packet(p)
                    # else:
                    #     AbcPacket.free(p)

    def waiting_packets(self) -> int:
        """Retorna o número de pacotes que estão esperando."""
        return len(self.arriving_packets)

    def invalidade_packets_over_this_edge(self, node_from: 'AbcNode', node_to: 'AbcNode', bidirectional: bool = False):
        has_edge = simulation.has_edge(node_from, node_to)

        if (not has_edge):
            return

        # Invalida os pacotes
        for packet in self.buffer:
            if ((packet.origin == node_from and packet.destination == node_to) or
                    (bidirectional and packet.origin == node_to and packet.destination == node_from)):
                packet.deny_delivery()

    def get_inbox(self) -> 'Inbox':
        """Obtém a Inbox com os pacotes que chegaram."""
        self.arriving_packets.sort(key=lambda p: p.arriving_time)
        if self.inbox is None:
            self.inbox = Inbox(self.arriving_packets)
        else:
            self.inbox.reset_for_list(self.arriving_packets)
        return self.inbox
