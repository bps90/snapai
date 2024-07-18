from typing import Type, Any
import importlib
from ..models.abc_connectivity_model import AbcConnectivityModel
from ..models.abc_mobility_model import AbcMobilityModel
from ..models.abc_interference_model import AbcInterferenceModel
from ..models.abc_reliability_model import AbcReliabilityModel
from ..models.abc_distribution_model import AbcDistributionModel
from ..models.nodes.abc_node_behavior import AbcNodeBehavior
from ..configuration.sim_config import sim_config_env
from abc import ABCMeta

class ModelsNormalizer:
    @staticmethod
    def normalize_mobility_model(mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str | None) -> AbcMobilityModel:
        if (mobility_model is None):
            mobility_model: Type[AbcMobilityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.mobility_models.{sim_config_env.mobility_model}').model

        elif (type(mobility_model) is str):
            mobility_model: Type[AbcMobilityModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'mobility_models.' + mobility_model).model

        if type(mobility_model) is type or type(mobility_model) is ABCMeta:
            mobility_model: AbcMobilityModel = mobility_model()

        return mobility_model

    @staticmethod
    def normalize_connectivity_model(connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str | None) -> AbcConnectivityModel:
        if (connectivity_model is None):
            connectivity_model: Type[AbcConnectivityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.connectivity_models.{sim_config_env.connectivity_model}').model

        elif (type(connectivity_model) is str):
            connectivity_model: Type[AbcConnectivityModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'connectivity_models.' + connectivity_model).model

        if type(connectivity_model) is type or type(connectivity_model) is ABCMeta:
            connectivity_model: AbcConnectivityModel = connectivity_model()

        return connectivity_model
    
    @staticmethod
    def normalize_interference_model(interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str | None) -> AbcInterferenceModel:
        if (interference_model is None):
            interference_model: Type[AbcInterferenceModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.interference_models.{sim_config_env.interference_model}').model

        elif (type(interference_model) is str):
            interference_model: Type[AbcInterferenceModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'interference_models.' + interference_model).model

        if type(interference_model) is type or type(interference_model) is ABCMeta:
            interference_model: AbcInterferenceModel = interference_model()

        return interference_model
    
    @staticmethod
    def normalize_reliability_model(reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str | None) -> AbcReliabilityModel:
        if (reliability_model is None):
            reliability_model: Type[AbcReliabilityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.reliability_models.{sim_config_env.reliability_model}').model

        elif (type(reliability_model) is str):
            reliability_model: Type[AbcReliabilityModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'reliability_models.' + reliability_model).model

        if type(reliability_model) is type or type(reliability_model) is ABCMeta:
            reliability_model: AbcReliabilityModel = reliability_model()

        return reliability_model

    @staticmethod
    def normalize_distribution_model(distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str | None) -> AbcDistributionModel:
        if (distribution_model is None):
            distribution_model: Type[AbcDistributionModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.distribution_models.{sim_config_env.distribution_model}').model

        elif (type(distribution_model) is str):
            distribution_model: Type[AbcDistributionModel] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'distribution_models.' + distribution_model).model

        if type(distribution_model) is type or type(distribution_model) is ABCMeta:
            distribution_model: AbcDistributionModel = distribution_model()

        return distribution_model

    @staticmethod
    def normalize_node_behavior_constructor(node_behavior_constructor: Type[AbcNodeBehavior] | str | None) -> Type[AbcNodeBehavior]:
        if (node_behavior_constructor is None):
            node_behavior_constructor: Type[AbcNodeBehavior] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.nodes.{sim_config_env.node_behavior}').node_behavior

        elif (type(node_behavior_constructor) is str):
            node_behavior_constructor: Type[AbcNodeBehavior] = importlib.import_module(
                sim_config_env.PROJECT_DIR.replace('/', '.') + 'nodes.' + node_behavior_constructor).node_behavior

        return node_behavior_constructor
