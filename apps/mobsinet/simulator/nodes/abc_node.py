from ..tools.position import Position
from ..models.abc_mobility_model import AbcMobilityModel

class AbcNode(object):

    def __init__(self, id):
        self.id = id
        self.position: Position = None
        self.mobility_model: AbcMobilityModel = None
        # self.connectivity_model: AbcConnectivityModel = None
        # self.interference_model: AbcInterferenceModel = None
        # self.reliability_model: AbcReliabilityModel = None

    def __str__(self):
        return f"""
        ID: {self.id}
        Position: {self.position}
        Mobility Model: {self.mobility_model.name}
        """
        