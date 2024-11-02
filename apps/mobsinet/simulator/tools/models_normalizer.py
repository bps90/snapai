from typing import Type, Any, TYPE_CHECKING
import importlib
from ..models.abc_connectivity_model import AbcConnectivityModel
from ..models.abc_mobility_model import AbcMobilityModel
from ..models.abc_interference_model import AbcInterferenceModel
from ..models.abc_reliability_model import AbcReliabilityModel
from ..models.abc_distribution_model import AbcDistributionModel

from ..configuration.sim_config import config
from abc import ABCMeta

if TYPE_CHECKING:
    from ..models.nodes.abc_node_implementation import AbcNodeImplementation


class ModelsNormalizer:
    @staticmethod
    def normalize_mobility_model(mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str | None) -> AbcMobilityModel:
        """(static) Normalizes the mobility model.

        Parameters
        ----------
        mobility_model : Type[AbcMobilityModel] | AbcMobilityModel | str | None
            The mobility model to normalize.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default mobility model will be returned.

        Returns
        -------
        AbcMobilityModel
            The normalized mobility model object.
        """

        if (mobility_model is None):
            mobility_model: Type[AbcMobilityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.mobility_models.{config.mobility_model}').model

        elif (type(mobility_model) is str):
            mobility_model: Type[AbcMobilityModel] = importlib.import_module(
                config.PROJECT_DIR.replace('/', '.') + 'mobility_models.' + mobility_model).model

        if type(mobility_model) is type or type(mobility_model) is ABCMeta:
            mobility_model: AbcMobilityModel = mobility_model()

        return mobility_model

    @staticmethod
    def normalize_connectivity_model(connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str | None) -> AbcConnectivityModel:
        """(static) Normalizes the connectivity model.

        Parameters
        ----------
        connectivity_model : Type[AbcConnectivityModel] | AbcConnectivityModel | str | None
            The connectivity model to normalize.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default connectivity model will be returned.

        Returns
        -------
        AbcConnectivityModel
            The normalized connectivity model object.
        """

        if (connectivity_model is None):
            connectivity_model: Type[AbcConnectivityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.connectivity_models.{config.connectivity_model}').model

        elif (type(connectivity_model) is str):
            connectivity_model: Type[AbcConnectivityModel] = importlib.import_module(
                config.PROJECT_DIR.replace('/', '.') + 'connectivity_models.' + connectivity_model).model

        if type(connectivity_model) is type or type(connectivity_model) is ABCMeta:
            connectivity_model: AbcConnectivityModel = connectivity_model()

        return connectivity_model

    @staticmethod
    def normalize_interference_model(interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str | None) -> AbcInterferenceModel:
        """(static) Normalizes the interference model.

        Parameters
        ----------
        interference_model : Type[AbcInterferenceModel] | AbcInterferenceModel | str | None
            The interference model to normalize.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default interference model will be returned.

        Returns
        -------
        AbcInterferenceModel
            The normalized interference model object.
        """

        if (interference_model is None):
            interference_model: Type[AbcInterferenceModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.interference_models.{config.interference_model}').model

        elif (type(interference_model) is str):
            interference_model: Type[AbcInterferenceModel] = importlib.import_module(
                config.PROJECT_DIR.replace('/', '.') + 'interference_models.' + interference_model).model

        if type(interference_model) is type or type(interference_model) is ABCMeta:
            interference_model: AbcInterferenceModel = interference_model()

        return interference_model

    @staticmethod
    def normalize_reliability_model(reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str | None) -> AbcReliabilityModel:
        """(static) Normalizes the reliability model.

        Parameters
        ----------
        reliability_model : Type[AbcReliabilityModel] | AbcReliabilityModel | str | None
            The reliability model to normalize.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default reliability model will be returned.

        Returns
        -------
        AbcReliabilityModel
            The normalized reliability model object.
        """

        if (reliability_model is None):
            reliability_model: Type[AbcReliabilityModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.reliability_models.{config.reliability_model}').model

        elif (type(reliability_model) is str):
            reliability_model: Type[AbcReliabilityModel] = importlib.import_module(
                config.PROJECT_DIR.replace('/', '.') + 'reliability_models.' + reliability_model).model

        if type(reliability_model) is type or type(reliability_model) is ABCMeta:
            reliability_model: AbcReliabilityModel = reliability_model()

        return reliability_model

    @staticmethod
    def normalize_distribution_model(distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str | None) -> AbcDistributionModel:
        """(static) Normalizes the distribution model.

        Parameters
        ----------
        distribution_model : Type[AbcDistributionModel] | AbcDistributionModel | str | None
            The distribution model to normalize.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default distribution model will be returned.

        Returns
        -------
        AbcDistributionModel
            The normalized distribution model object.
        """

        if (distribution_model is None):
            distribution_model: Type[AbcDistributionModel] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.distribution_models.{config.distribution_model}').model

        elif (type(distribution_model) is str):
            distribution_model: Type[AbcDistributionModel] = importlib.import_module(
                config.PROJECT_DIR.replace('/', '.') + 'distribution_models.' + distribution_model).model

        if type(distribution_model) is type or type(distribution_model) is ABCMeta:
            distribution_model: AbcDistributionModel = distribution_model()

        return distribution_model

    @staticmethod
    def normalize_node_implementation_constructor(node_implementation_constructor: Type['AbcNodeImplementation'] | str | None) -> Type['AbcNodeImplementation']:
        """Normalizes the node implementation constructor.

        Parameters
        ----------
        node_implementation_constructor : Type[AbcNodeImplementation] | str | None
            The node implementation constructor to normalize.
            If a string, it must be exactly the name of the file containing the node_implementation,
            without the ".py" extension; it will be imported from PROJECT_DIR.
            If None, the default node implementation constructor will be returned.

        Returns
        -------
        Type[AbcNodeImplementation]
            The normalized node implementation constructor.
        """

        if (node_implementation_constructor is None):
            node_implementation_constructor: Type['AbcNodeImplementation'] = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.nodes.{config.node_implementation}').node_implementation

        elif (type(node_implementation_constructor) is str):
            node_implementation_constructor: Type['AbcNodeImplementation'] = importlib.import_module(
                config.PROJECT_DIR.replace('/', '.') + 'nodes.' + node_implementation_constructor).node_implementation

        return node_implementation_constructor
