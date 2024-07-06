import networkx as nx

# tracking available id

class NetworkSimulator(object):
    

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.id_counter = 0

    def add_node(self, node_id = None):

        if node_id not in self.graph.nodes():
            self.graph.add_node(node_id)
        else:
            raise ValueError(f"Node with ID {node_id} already exists.")
        
        """print(self.graph.nodes())
        print(self.id_counter)

        if node_id is None: # find a available ID to use
            while True:
                if self.id_counter not in self.graph.nodes(): 
                    self.id_counter += 1
                    self.graph.add_node(self.id_counter)
                    return
                else:
                    self.id_counter += 1
        
        if isinstance(node_id, int) and node_id not in self.graph.nodes():
            self.graph.add_node(node_id)
        elif node_id not in self.graph.nodes():
            self.graph.add_node(node_id)
        else:
            raise ValueError(f"Node with ID {node_id} already exists.")"""

    def remove_node(self, node_id):
        if node_id in self.graph.nodes():
            self.graph.remove_node(node_id)
        else:
            raise ValueError(f"Node with ID {node_id} already removed or do not exists.")

    def add_edge(self, from_id, to_id):
        self.graph.add_edge(from_id, to_id)

    def add_bi_directional_edge(self, id1, id2):
        self.add_edge(id1, id2)
        self.add_edge(id2, id1)

    def remove_edge(self ,  from_id, to_id):
        self.graph.remove_edge(from_id, to_id)
    
    def remove_bi_directional_edge(self, id1, id2):
        self.remove_edge(id1, id2)
        self.remove_edge(id2, id1)
    
    def set_net_models():
        pass

    def __str__(self) -> str:
        return str(self.graph)
    
    



if __name__ == "__main__":
    # Create instances of the class
    ns = NetworkSimulator()
    for i in range(1, 4):
        ns.add_node(i)

    ns.add_bi_directional_edge(1, 4)
    ns.add_edge(2,3)
    print(ns.graph.edges())
    ns.remove_bi_directional_edge(1, 4)
    print(ns.graph.edges())
    print(ns)
    print(ns.graph.nodes())