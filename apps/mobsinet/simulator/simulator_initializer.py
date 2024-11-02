# THIS FILE IS TEMPORARY AND SHOULD BE REMOVED AFTERWARDS

from .global_vars import Global
from .network_simulator import simulation
from .tools.models_normalizer import ModelsNormalizer

Global.is_gui_mode = False
Global.use_project = False
Global.message_transmission_model = ModelsNormalizer.normalize_message_transmission_model()
Global.custom_global.check_project_requirements()

simulation.init_simulator(parameters={
    "refresh_rate": 1,
    "number_of_nodes": 10,
    "distribution_model": "linear_dist",
    "node_implementation_constructor": "inert_node_implementation",
    "mobility_model": "random_walk",
    "connectivity_model": "qudg_connectivity",
    "interference_model": "no_interference",
    "reliability_model": "reliable_delivery"
})

simulation.pre_run()

simulation.run()