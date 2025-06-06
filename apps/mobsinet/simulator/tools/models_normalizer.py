import importlib

from typing import Type, TYPE_CHECKING
from ..configuration.sim_config import config
from abc import ABCMeta

if TYPE_CHECKING:
    from ..models.nodes.abc_node import AbcNode
    from ..models.abc_message_transmission_model import AbcMessageTransmissionModel
    from ..models.abc_mobility_model import AbcMobilityModel
    from ..models.abc_connectivity_model import AbcConnectivityModel
    from ..models.abc_interference_model import AbcInterferenceModel
    from ..models.abc_reliability_model import AbcReliabilityModel
    from ..models.abc_distribution_model import AbcDistributionModel




class ModelsNormalizer:
    @staticmethod
    def normalize_mobility_model(mobility_model: Type['AbcMobilityModel'] | 'AbcMobilityModel' | str | None) -> 'AbcMobilityModel':
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
            mobility_model = config.mobility_model

        if (type(mobility_model) is str):
            if (mobility_model.__contains__(':')):
                project_name, mobility_model = mobility_model.split(':')
                
                mobility_model: Type['AbcMobilityModel'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.mobility_models.' + mobility_model).model
            else:
                mobility_model: Type['AbcMobilityModel'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.mobility_models.{mobility_model}').model
            

        if type(mobility_model) is type or type(mobility_model) is ABCMeta:
            mobility_model: 'AbcMobilityModel' = mobility_model()

        return mobility_model
    
    @staticmethod
    def normalize_message_transmission_model(message_transmission_model: Type['AbcMessageTransmissionModel'] | 'AbcMessageTransmissionModel' | str | None) -> 'AbcMessageTransmissionModel':
        """(static) Normalizes the message transmission model.

        Parameters
        ----------
        message_transmission_model : Type[AbcMessageTransmissionModel] | AbcMessageTransmissionModel | str | None
            The message transmission model to normalize.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default message transmission model will be returned.

        Returns
        -------
        AbcMessageTransmissionModel
            The normalized message transmission model object.
        """

        if (message_transmission_model is None):
            message_transmission_model = config.message_transmission_model

        if (type(message_transmission_model) is str):
            if (message_transmission_model.__contains__(':')):
                project_name, message_transmission_model = message_transmission_model.split(':')
                
                message_transmission_model: Type['AbcMessageTransmissionModel'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.message_transmission_models.' + message_transmission_model).model
            else:
                message_transmission_model: Type['AbcMessageTransmissionModel'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.message_transmission_models.{message_transmission_model}').model

        if type(message_transmission_model) is type or type(message_transmission_model) is ABCMeta:
            message_transmission_model: 'AbcMessageTransmissionModel' = message_transmission_model()

        return message_transmission_model

    @staticmethod
    def normalize_connectivity_model(connectivity_model: Type['AbcConnectivityModel'] | 'AbcConnectivityModel' | str | None) -> 'AbcConnectivityModel':
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
            connectivity_model = config.connectivity_model

        if (type(connectivity_model) is str):
            if (connectivity_model.__contains__(':')):
                project_name, connectivity_model = connectivity_model.split(':')
                
                connectivity_model: Type['AbcConnectivityModel'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.connectivity_models.' + connectivity_model).model
            else:
                connectivity_model: Type['AbcConnectivityModel'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.connectivity_models.{connectivity_model}').model
            
            

        if type(connectivity_model) is type or type(connectivity_model) is ABCMeta:
            connectivity_model: 'AbcConnectivityModel' = connectivity_model()

        return connectivity_model

    @staticmethod
    def normalize_interference_model(interference_model: Type['AbcInterferenceModel'] | 'AbcInterferenceModel' | str | None) -> 'AbcInterferenceModel':
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
            interference_model = config.interference_model

        if (type(interference_model) is str):
            if (interference_model.__contains__(':')):
                project_name, interference_model = interference_model.split(':')
                
                interference_model: Type['AbcInterferenceModel'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.interference_models.' + interference_model).model
            else:
                interference_model: Type['AbcInterferenceModel'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.interference_models.{interference_model}').model

        if type(interference_model) is type or type(interference_model) is ABCMeta:
            interference_model: 'AbcInterferenceModel' = interference_model()

        return interference_model

    @staticmethod
    def normalize_reliability_model(reliability_model: Type['AbcReliabilityModel'] | 'AbcReliabilityModel' | str | None) -> 'AbcReliabilityModel':
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
            reliability_model = config.reliability_model

        if (type(reliability_model) is str):
            if (reliability_model.__contains__(':')):
                project_name, reliability_model = reliability_model.split(':')
                
                reliability_model: Type['AbcReliabilityModel'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.reliability_models.' + reliability_model).model
            else:
                reliability_model: Type['AbcReliabilityModel'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.reliability_models.{reliability_model}').model
            

        if type(reliability_model) is type or type(reliability_model) is ABCMeta:
            reliability_model: 'AbcReliabilityModel' = reliability_model()

        return reliability_model

    @staticmethod
    def normalize_distribution_model(distribution_model: Type['AbcDistributionModel'] | 'AbcDistributionModel' | str | None) -> 'AbcDistributionModel':
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
            distribution_model = config.distribution_model

        if (type(distribution_model) is str):
            if (distribution_model.__contains__(':')):
                project_name, distribution_model = distribution_model.split(':')
                
                distribution_model: Type['AbcDistributionModel'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.distribution_models.' + distribution_model).model
            else:
                distribution_model: Type['AbcDistributionModel'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.distribution_models.{distribution_model}').model

        if type(distribution_model) is type or type(distribution_model) is ABCMeta:
            distribution_model: 'AbcDistributionModel' = distribution_model()

        return distribution_model

    @staticmethod
    def normalize_node_constructor(node_constructor: Type['AbcNode'] | str | None) -> Type['AbcNode']:
        """Normalizes the node constructor.

        Parameters
        ----------
        node_constructor : Type[AbcNode] | str | None
            The node constructor to normalize.
            If a string, it must be exactly the name of the file containing the node implementation,
            without the ".py" extension; it will be imported from PROJECT_DIR.
            If None, the default node constructor will be returned.

        Returns
        -------
        Type[AbcNode]
            The normalized node constructor.
        """

        if (node_constructor is None):
            node_constructor = config.node

        if (type(node_constructor) is str):
            if (node_constructor.__contains__(':')):
                project_name, node_constructor = node_constructor.split(':')
                
                node_constructor: Type['AbcNode'] = importlib.import_module(
                    config.PROJECT_DIR.replace('/', '.') + project_name + '.nodes.' + node_constructor).node
            else:
                node_constructor: Type['AbcNode'] = importlib.import_module(
                    f'apps.mobsinet.simulator.defaults.nodes.{node_constructor}').node
        return node_constructor
