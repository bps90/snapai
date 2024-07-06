from .mobility_model import MobilityModelQueryDataInspector, MobilityModelQueryData

class RandomWalkQueryData(MobilityModelQueryData):
    pass

class RandomWalkQueryDataInspector(MobilityModelQueryDataInspector):
    def get_query_data(self) -> RandomWalkQueryData:
        return RandomWalkQueryData(self.nodes_qty, self.simulation_time, self.scenario_dimensions, self.scenario_size_x, self.scenario_size_y, self.scenario_size_z)