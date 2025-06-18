import random
from ...models.nodes.abc_node import AbcNode
from ...models.abc_connectivity_model import AbcConnectivityModel
from ...configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionNumberField, FormSectionPercentageField, FormSectionFieldInformative
from typing import TypedDict


class QUDGConnectivityParameters(TypedDict):
    sure_connection_radius: float
    unsure_connection_radius: float
    unsure_radius_probability: float


class QUDGConnectivity(AbcConnectivityModel):
    form_subsection_layout = FormSubSection('qudg_connectivity_parameters_subsection').add_line(
        FormSectionLine().add_fields([
            FormSectionNumberField(
                id="qudg_connectivity_sure_connection_radius",
                label="Sure Connection Radius",
                name="sure_connection_radius",
                occuped_columns=4,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The radius of a node having a sure connection.",
                ),
            ),
            FormSectionNumberField(
                id="qudg_connectivity_unsure_connection_radius",
                label="Unsure Connection Radius",
                name="unsure_connection_radius",
                occuped_columns=4,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The radius of a node having an unsure connection.",
                ),
            ),
            FormSectionPercentageField(
                id="qudg_connectivity_unsure_radius_probability",
                label="Unsure Radius Probability",
                name="unsure_radius_probability",
                occuped_columns=4,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The probability of a node having a connection while being in the unsure radius",
                ),
            ),
        ])
    )

    def __init__(self, parameters: QUDGConnectivityParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)

        self.set_parameters(parameters)

    def check_parameters(self, parameters) -> bool:
        if ('sure_connection_radius' not in parameters or
            parameters['sure_connection_radius'] is None or
            parameters['sure_connection_radius'] < 0 or
                (type(parameters['sure_connection_radius']) != float and type(parameters['sure_connection_radius']) != int)):
            return False

        if ('unsure_connection_radius' not in parameters or
            parameters['unsure_connection_radius'] is None or
            parameters['unsure_connection_radius'] < 0 or
            (type(parameters['unsure_connection_radius']) != float and type(parameters['unsure_connection_radius']) != int) or
                parameters['unsure_connection_radius'] < parameters['sure_connection_radius']):
            return False

        if ('unsure_radius_probability' not in parameters or
            parameters['unsure_radius_probability'] is None or
            parameters['unsure_radius_probability'] < 0 or
                parameters['unsure_radius_probability'] > 1):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: QUDGConnectivityParameters = parameters
        self.sure_connection_radius: float = parsed_parameters['sure_connection_radius']
        self.unsure_connection_radius: float = parsed_parameters['unsure_connection_radius']
        self.unsure_radius_probability: float = parsed_parameters['unsure_radius_probability']

    def is_connected(self, node_a: AbcNode, node_b: AbcNode) -> bool:
        distance_between_nodes = node_a.position.euclidean_distance(
            node_b.position)

        if (distance_between_nodes <= self.sure_connection_radius):
            return True
        elif (distance_between_nodes <= self.unsure_connection_radius):
            return True if (random.random() < self.unsure_radius_probability) else False

        return False

    def set_unsure_connection_radius(self, radius: int):

        if radius < 0:
            raise ValueError('The radius must be positive.')

        self.unsure_connection_radius = radius

    def set_sure_connection_radius(self, radius: int):
        if radius < 0:
            raise ValueError('The radius must be positive.')

        self.sure_connection_radius = radius

    def set_unsure_radius_probability(self, probability: float):

        if (probability < 0 or probability > 1):
            raise ValueError('The probability must be between 0 and 1.')

        self.unsure_radius_probability = probability


model = QUDGConnectivity
