from typing import TYPE_CHECKING
from ...models.abc_connectivity_model import AbcConnectivityModel
from ...configuration.layout.form_section import FormSubSection

if TYPE_CHECKING:
    from ...models.nodes.abc_node import AbcNode


class NoConnectivity(AbcConnectivityModel):
    form_subsection_layout = FormSubSection(
        'no_connectivity_parameters_subsection')

    def is_connected(self, node_a: 'AbcNode', node_b: 'AbcNode') -> bool:
        """Check if the nodes are connected."""
        return False

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass


model = NoConnectivity
