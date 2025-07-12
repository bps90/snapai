from ...models.nodes.packet import Packet
from ...models.abc_reliability_model import AbcReliabilityModel
from typing import TypedDict
from ...configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionFieldInformative, FormSectionPercentageField
import random


class ProbabilisticReliabilityParameters(TypedDict):
    success_probability: float

class ProbabilisticReliability(AbcReliabilityModel):
    form_subsection_layout = FormSubSection(
        id="probabilistic_reliability_parameters_subsection",
    ).add_line(
        FormSectionLine().add_field(
            FormSectionPercentageField(
                id="probabilistic_reliability_success_probability",
                label="Success Probability",
                name="success_probability",
                occuped_columns=12,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The probability that the packet will be delivered to the destination node.",
                ),
            )
        )
    )
    
    def __init__(self, parameters: ProbabilisticReliabilityParameters):
        super().__init__(parameters)
        self.set_parameters(parameters)
        
    def check_parameters(self, parameters):
        if ('success_probability' not in parameters or 
            (not isinstance(parameters['success_probability'], float) and not isinstance(parameters['success_probability'], int)) or
            parameters['success_probability'] < 0 or
            parameters['success_probability'] > 100):
            return False
    
        return True
    
    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')
        
        parsed_parameters: ProbabilisticReliabilityParameters = parameters
        
        self.success_probability = parsed_parameters['success_probability']

    def reaches_destination(self, packet: Packet):
        return random.random() * 100 < self.success_probability

        
model = ProbabilisticReliability
