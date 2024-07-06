from abc import ABC, abstractmethod
from ..query_parsers.mobility_model import MobilityModelQuery
from ..generator.Simulation import SimulationData

class MobilityModelQueryData(SimulationData):
    def __init__(self, nodes_qty: int, simulation_time: int, scenario_dimensions: int, scenario_size_x: int, scenario_size_y: int, scenario_size_z: int):
        self.nodes_qty = nodes_qty
        self.simulation_time = simulation_time
        self.scenario_dimensions = scenario_dimensions
        self.scenario_size = (scenario_size_x, scenario_size_y, scenario_size_z)

class MobilityModelQueryDataInspector(ABC):
    default_scenario_dimensions = 3

    def __init__(self, query: MobilityModelQuery):
        self.nodes_qty = query.nodes_qty
        self.simulation_time = query.simulation_time
        self.scenario_dimensions = query.scenario_dimensions
        self.scenario_size_x = query.scenario_size_x
        self.scenario_size_y = query.scenario_size_y
        self.scenario_size_z = query.scenario_size_z
        self._insertdefaults()
        self._inspect()

    def _insertdefaults(self):
        if self.scenario_dimensions is None: self.scenario_dimensions = self.default_scenario_dimensions
        if self.scenario_size_y is None: self.scenario_size_y = 0
        if self.scenario_size_z is None: self.scenario_size_z = 0

    def _inspect(self):
        """ Validate nodes_qty is a positive integer """
        if self.nodes_qty <= 0:
            raise Exception('Nodes Qty must be a positive integer')
        
        """ Validate simulation_time is a non-negative integer """
        if self.simulation_time < 0:
            raise Exception('Simulation Time must be a non-negative integer')
        
        """ Validate scenario_dimensions is between 1 and 3 """
        if self.scenario_dimensions < 1 or self.scenario_dimensions > 3:
            raise Exception('Scenario Dimensions must be between 1 and 3')
        
        """ Validate scenario_size_x is a positive integer """
        if self.scenario_size_x <= 0:
            raise Exception('Scenario Size X must be a positive integer')
        
        """ Validate scenario_size_y is a non-negative integer """
        if self.scenario_size_y < 0:
            raise Exception('Scenario Size Y must be a non-negative integer')
        
        """ Validate scenario_size_z is a non-negative integer """
        if self.scenario_size_z < 0:
            raise Exception('Scenario Size Z must be a non-negative integer')
        
    @abstractmethod
    def get_query_data(self) -> MobilityModelQueryData:
        pass