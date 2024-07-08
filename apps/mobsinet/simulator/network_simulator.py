import importlib.util
import networkx as nx
import importlib
import sys

from .models.abc_distribution_model import AbcDistributionModel
from .configuration.sim_config import sim_config_env

class NetworkSimulator(object):
    

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.dist_model = None

    def add_node(self, node_id = None):

        if node_id not in self.graph.nodes():
            self.graph.add_node(node_id)
        else:
            raise ValueError(f"Node with ID {node_id} already exists.")
        
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

    def remove_edge(self,  from_id, to_id):
        self.graph.remove_edge(from_id, to_id)
    
    def remove_bi_directional_edge(self, id1, id2):
        self.remove_edge(id1, id2)
        self.remove_edge(id2, id1)
    
    def int_net_models(self):
        """Init the models that will be used in the simulation."""

        #dist_model:AbcDistributionModel  = importlib.util.spec_from_file_location("random_dist", "/Users/bps/Documents/playground/MobENV/apps/mobsinet/simulator/defaults/distribution_models/random_dist.py")
        #foo = importlib.util.module_from_spec(dist_model)
        #sys.modules["random_dist"] = foo
        #dist_model.loader.exec_module(foo)
        #print(foo.RandomDist())
        pass

    def run(self):
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
    ns.int_net_models()