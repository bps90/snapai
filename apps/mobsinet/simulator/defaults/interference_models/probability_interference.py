from ...models.abc_interference_model import AbcInterferenceModel
from ...models.nodes.packet import Packet
import random
from typing import Any, TypedDict


class ProbabilityInterferenceParameters(TypedDict):
    intensity: float


class ProbabilityInterference(AbcInterferenceModel):
    def __init__(self, parameters: ProbabilityInterferenceParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

    def check_parameters(self, parameters):
        if ('intensity' not in parameters or
                (not isinstance(parameters['intensity'], int) and not isinstance(parameters['intensity'], float)) or
                parameters['intensity'] < 0 or parameters['intensity'] > 100):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: ProbabilityInterferenceParameters = parameters
        self.intensity: float = parsed_parameters['intensity']

    def set_intensity(self, intensity: int):
        self.intensity = intensity

    def is_disturbed(self, packet: Packet) -> bool:
        return random.randint(0, 100) < self.intensity


model = ProbabilityInterference
