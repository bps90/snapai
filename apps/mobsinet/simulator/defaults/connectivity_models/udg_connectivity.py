from ...models.nodes.abc_node import AbcNode
from ...models.abc_connectivity_model import AbcConnectivityModel
from typing import TypedDict
from ...configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionNumberField, FormSectionPercentageField, FormSectionFieldInformative


class UDGConnectivityParameters(TypedDict):
    radius: int


class UDGConnectivity(AbcConnectivityModel):
    form_subsection_layout = FormSubSection('udg_connectivity_parameters_subsection').add_line(
        FormSectionLine().add_fields([
            FormSectionNumberField(
                id="udg_connectivity_radius",
                label="Connection Radius",
                name="radius",
                occuped_columns=4,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The radius of a node having a connection.",
                ),
            )
        ])
    )

    def __init__(self, parameters: UDGConnectivityParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

    def check_parameters(self, parameters):
        if ('radius' not in parameters or
            parameters['radius'] is None or
            parameters['radius'] < 0 or
                (type(parameters['radius']) != float and type(parameters['radius']) != int)):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: UDGConnectivityParameters = parameters
        self.radius: float = parsed_parameters['radius']

    def is_connected(self, node_a: AbcNode, node_b: AbcNode) -> bool:
        """Check if the nodes are connected.
        Nodes are connected if their distance is less than or equal to the maximum radius.

        """
        distance_between_nodes = node_a.position.euclidean_distance(
            node_b.position)

        if (distance_between_nodes <= self.radius):
            return True

        return False

    def set_radius(self, radius: int):
        """Set the maximum radius that the nodes can be connected.

        Parameters
        ----------
        radius : int
            The maximum radius in unit of length.

        Raises
        ------
        ValueError
            If the radius is negative.
        """

        if radius < 0:
            raise ValueError('The radius must be positive.')

        self.radius = radius


model = UDGConnectivity
