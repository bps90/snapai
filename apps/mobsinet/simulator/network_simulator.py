import importlib.util
import networkx as nx
import importlib
import sys

from .models.abc_distribution_model import AbcDistributionModel
from .models.abc_mobility_model import AbcMobilityModel
from .models.abc_connectivity_model import AbcConnectivityModel
from .models.abc_interference_model import AbcInterferenceModel
from .models.abc_reliability_model import AbcReliabilityModel
from .nodes.abc_node import AbcNode
from .tools.position import Position
from .configuration.sim_config import sim_config_env
from typing import Type, Any

from .defaults.mobility_models.random_mob import model
from abc import ABCMeta

class NetworkSimulator(object):

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.dist_model = None

    
    def add_nodes(
        self,
        nodes: int | list[Any],
        distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str | None = None,
        node_constructor: Type[AbcNode] | str | None = None,
        mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str | None = None,
        connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str | None = None,
        interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str | None = None,
        reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str | None = None,
    ):
        
        distribution_model = self._normalize_distribution_model(distribution_model)

    
        for id in (range(nodes) if type(nodes) is int else nodes):
            position = distribution_model.get_position()

            self.add_node(
                position=position,
                node_id=id if type(nodes) is not int else None,
                node_constructor=node_constructor,
                mobility_model=mobility_model,
                connectivity_model=connectivity_model,
                interference_model=interference_model,
                reliability_model=reliability_model
            )

    def add_node(
        self,
        position: Position,
        node_id=None,
        node_constructor: Type[AbcNode] | str | None = None,
        mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str | None = None,
        connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str | None = None,
        interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str | None = None,
        reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str | None = None,
    ):

        mobility_model = self._normalize_mobility_model(mobility_model)
        connectivity_model = self._normalize_connectivity_model(connectivity_model)
        interference_model = self._normalize_interference_model(interference_model)
        reliability_model = self._normalize_reliability_model(reliability_model)
        node_constructor = self._normalize_node_constructor(node_constructor)
        position: Position = position or importlib.import_module('apps.mobsinet.simulator.defaults.distribution_models.' + sim_config_env.distribution_model).model().get_position()

        if (not node_id):
            node_id = self._gen_node_id()

        if node_id not in self.graph.nodes():
            self.graph.add_node(
                node_id,
                node=node_constructor(
                    node_id,
                    position=position,
                    mobility_model=mobility_model,
                    connectivity_model=connectivity_model,
                    interference_model=interference_model,
                    reliability_model=reliability_model),
            )
        else:
            raise ValueError(f"Node with ID {node_id} already exists.")


    def remove_node(self, node_id):
        if node_id in self.graph.nodes():
            self.graph.remove_node(node_id)
        else:
            raise ValueError(
                f"Node with ID {node_id} already removed or do not exists.")

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

    def init_net_models(self):
        """Init the models that will be used in the simulation."""

        # dist_model:AbcDistributionModel  = importlib.util.spec_from_file_location("random_dist", "/Users/bps/Documents/playground/MobENV/apps/mobsinet/simulator/defaults/distribution_models/random_dist.py")
        # foo = importlib.util.module_from_spec(dist_model)
        # sys.modules["random_dist"] = foo
        # dist_model.loader.exec_module(foo)
        # print(foo.RandomDist())
        pass

    def run(self):
        pass

    def __str__(self) -> str:
        return str(self.graph)

    def _gen_node_id(self):
        """ Generates a new node_id based on number of current nodes in the graph. """
        node_id = self.graph.number_of_nodes() + 1

        while node_id in self.graph.nodes():
            node_id += 1

        return node_id
    
    def _normalize_mobility_model(self, mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str | None) -> AbcMobilityModel:
        if (mobility_model is None):
            mobility_model: Type[AbcMobilityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.mobility_models.{sim_config_env.mobility_model}').model

        elif (type(mobility_model) is str):
            mobility_model: Type[AbcMobilityModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'mobility_models.' + mobility_model).model

        if type(mobility_model) is type or type(mobility_model) is ABCMeta:
            mobility_model: AbcMobilityModel = mobility_model()

        return mobility_model

    def _normalize_connectivity_model(self, connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str | None) -> AbcConnectivityModel:
        if (connectivity_model is None):
            connectivity_model: Type[AbcConnectivityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.connectivity_models.{sim_config_env.connectivity_model}').model

        elif (type(connectivity_model) is str):
            connectivity_model: Type[AbcConnectivityModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'connectivity_models.' + connectivity_model).model

        if type(connectivity_model) is type or type(connectivity_model) is ABCMeta:
            connectivity_model: AbcConnectivityModel = connectivity_model()

        return connectivity_model
    
    def _normalize_interference_model(self, interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str | None) -> AbcInterferenceModel:
        if (interference_model is None):
            interference_model: Type[AbcInterferenceModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.interference_models.{sim_config_env.interference_model}').model

        elif (type(interference_model) is str):
            interference_model: Type[AbcInterferenceModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'interference_models.' + interference_model).model

        if type(interference_model) is type or type(interference_model) is ABCMeta:
            interference_model: AbcInterferenceModel = interference_model()

        return interference_model
    
    def _normalize_reliability_model(self, reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str | None) -> AbcReliabilityModel:
        if (reliability_model is None):
            reliability_model: Type[AbcReliabilityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.reliability_models.{sim_config_env.reliability_model}').model

        elif (type(reliability_model) is str):
            reliability_model: Type[AbcReliabilityModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'reliability_models.' + reliability_model).model

        if type(reliability_model) is type or type(reliability_model) is ABCMeta:
            reliability_model: AbcReliabilityModel = reliability_model()

        return reliability_model

    def _normalize_distribution_model(self, distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str | None) -> AbcDistributionModel:
        if (distribution_model is None):
            distribution_model: Type[AbcDistributionModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.distribution_models.{sim_config_env.distribution_model}').model

        elif (type(distribution_model) is str):
            distribution_model: Type[AbcDistributionModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'distribution_models.' + distribution_model).model

        if type(distribution_model) is type or type(distribution_model) is ABCMeta:
            distribution_model: AbcDistributionModel = distribution_model()

        return distribution_model

    def _normalize_node_constructor(self, node_constructor: Type[AbcNode] | str | None) -> Type[AbcNode]:
        if (node_constructor is None):
            node_constructor: Type[AbcNode] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.nodes.{sim_config_env.node}').node

        elif (type(node_constructor) is str):
            node_constructor: Type[AbcNode] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'nodes.' + node_constructor).node

        return node_constructor

    

if __name__ == "__main__":
    # Create instances of the class
    ns = NetworkSimulator()
    # for i in range(1, 4):
    #     ns.add_node(i)

    ns.add_nodes([1,2,3,4])

    ns.add_bi_directional_edge(1, 4)
    ns.add_edge(2,3)
    print(ns.graph.edges())
    ns.remove_bi_directional_edge(1, 4)
    print(ns.graph.edges())
    print(ns)
    print(ns.graph.nodes())
    ns.init_net_models()

    # dist_model  = importlib.util.spec_from_file_location("random_dist", "apps/mobsinet/simulator/defaults/distribution_models/random_dist.py")
    # foo = importlib.util.module_from_spec(dist_model)
    # sys.modules["random_dist"] = foo
    # dist_model.loader.exec_module(foo)

    # print(foo)

    # randomDistModule = importlib.import_module(
    #     'apps.mobsinet.simulator.defaults.distribution_models.random_dist')

    # print(randomDistModule.model())

    print('\nGraph nodes with his attributes')
    print(ns.graph.nodes(data=True))
