from ...models.abc_interference_model import AbcInterferenceModel
from ...models.nodes.packet import Packet
import random
from typing import TypedDict
from ...configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionPercentageField, FormSectionFieldInformative

class ProbabilityInterferenceParameters(TypedDict):
    intensity: float


class ProbabilityInterference(AbcInterferenceModel):
    form_subsection_layout = FormSubSection(
        id="probability_interference_parameters_subsection",
    ).add_line(
        FormSectionLine().add_field(
            FormSectionPercentageField(
                id="probability_interference_intensity",
                label="Intensity",
                name="intensity",
                occuped_columns=12,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The intensity of the interference. The higher the intensity, the more likely the packet will be disturbed.",
                ),
            )
        )
    )
    
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
