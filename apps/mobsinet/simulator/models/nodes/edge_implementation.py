# GENERATED WITH HELP FROM CHATGPT

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .abc_node_implementation import AbcNodeImplementation
    from .abc_message import AbcMessage

class EdgeImplementation:
    num_edges_on_the_fly = 0

    def __init__(self, start_node: 'AbcNodeImplementation' = None, end_node: 'AbcNodeImplementation' = None):
        self.start_node = start_node
        self.end_node = end_node
        self.opposite_edge: 'EdgeImplementation' = None
        self.number_of_messages_on_this_edge = 0
        self.valid = False
        
        self.find_opposite_edge()
        self.initialize_edge()
        EdgeImplementation.num_edges_on_the_fly += 1


    def initialize_edge(self):
        pass

    def clean_up(self):
        pass

    def get_number_of_messages_on_this_edge(self):
        return self.number_of_messages_on_this_edge

    def get_opposite_edge(self):
        return self.opposite_edge

    def equals(self, edge):
        return (self.start_node.id == edge.start_node.id and
                self.end_node.id == edge.end_node.id)


    def find_opposite_edge(self):
        for edge in self.end_node.outgoing_connections:
            if edge.start_node.id == self.end_node.id and edge.end_node.id == self.start_node.id:
                self.opposite_edge = edge
                edge.opposite_edge = self
                return
        self.opposite_edge = None

    def add_message_for_this_edge(self, msg: 'AbcMessage'):
        self.number_of_messages_on_this_edge += 1

    def remove_message_for_this_edge(self, msg: 'AbcMessage'):
        self.number_of_messages_on_this_edge -= 1
