from ...models.abc_interference_model import AbcInterferenceModel
from ...models.nodes.packet import Packet
import random
from ...configuration.sim_config import config


class ProbabilityInterference(AbcInterferenceModel):
    def __init__(self):
        super().__init__('ProbabilityInterference')
        self.intensity = config.interference_model_parameters['intensity']

    def set_intensity(self, intensity: int):
        self.intensity = intensity

    def is_disturbed(self, packet: Packet) -> bool:
        return random.randint(0, 100) < self.intensity


model = ProbabilityInterference
