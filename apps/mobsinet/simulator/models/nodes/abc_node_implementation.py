from ...tools.position import Position
from ..abc_mobility_model import AbcMobilityModel
from ..abc_connectivity_model import AbcConnectivityModel
from ..abc_interference_model import AbcInterferenceModel
from ..abc_reliability_model import AbcReliabilityModel
from abc import ABC


class AbcNodeImplementation(ABC):

    def __init__(
            self,
            id: int,
            position: Position = None,
            mobility_model: AbcMobilityModel = None,
            connectivity_model: AbcConnectivityModel = None,
            interference_model: AbcInterferenceModel = None,
            reliability_model: AbcReliabilityModel = None):
        self.id = id
        self.position: Position = position
        self.mobility_model: AbcMobilityModel = mobility_model
        self.connectivity_model: AbcConnectivityModel = connectivity_model
        self.interference_model: AbcInterferenceModel = interference_model
        self.reliability_model: AbcReliabilityModel = reliability_model

    def __str__(self):
        return f"""
ID: {self.id}
Position: {self.position}
Mobility Model: {self.mobility_model.name}
Connectivity Model: {self.connectivity_model.name}
Interference Model: {self.interference_model.name}
Reliability Model: {self.reliability_model.name}
"""

    def __repr__(self) -> str:
        return self.__str__()

    def set_position(self, position: Position):
        self.position = position

    def set_mobility_model(self, mobility_model: AbcMobilityModel):
        self.mobility_model = mobility_model

    def set_connectivity_model(self, connectivity_model: AbcConnectivityModel):
        self.connectivity_model = connectivity_model

    def set_interference_model(self, interference_model: AbcInterferenceModel):
        self.interference_model = interference_model

    def set_reliability_model(self, reliability_model: AbcReliabilityModel):
        self.reliability_model = reliability_model

    def get_coordinates(self):
        return self.position.get_coordinates()

    def set_coordinates(self, x: int, y: int, z: int):
        return self.position.set_coordinates(x, y, z)
