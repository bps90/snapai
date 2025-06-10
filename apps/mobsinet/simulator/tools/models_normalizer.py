import importlib

from typing import Type, TYPE_CHECKING, Optional
from ..configuration.sim_config import SimulationConfig
from abc import ABCMeta

if TYPE_CHECKING:
    from ..models.nodes.abc_node import AbcNode
    from ..models.abc_message_transmission_model import AbcMessageTransmissionModel
    from ..models.abc_mobility_model import AbcMobilityModel
    from ..models.abc_connectivity_model import AbcConnectivityModel
    from ..models.abc_interference_model import AbcInterferenceModel
    from ..models.abc_reliability_model import AbcReliabilityModel
    from ..models.abc_distribution_model import AbcDistributionModel


class ModelsSearchEngine:
    @staticmethod
    def find_message_transmission_model(message_transmission_model_arg: Optional[str]) -> 'Type[AbcMessageTransmissionModel]':
        """(static) Finds the message transmission model.

        Parameters
        ----------
        message_transmission_model : Optional[str]
            The message transmission model to find, it must be exactly the name of the file containing the 
            model - or the project name and the model name, separated by a ":" -
            without the ".py" extension

            it will be imported from PROJECTS_DIR and instantiated.
            If None, the configured message transmission model will be returned.

        Returns
        -------
        Type[AbcMessageTransmissionModel]
            The message transmission model class.
        """

        if (message_transmission_model_arg is None):
            message_transmission_model_arg = SimulationConfig.message_transmission_model

        if (message_transmission_model_arg.__contains__(':')):
            project_name, message_transmission_model_name = message_transmission_model_arg.split(
                ':')

            message_transmission_model: Type['AbcMessageTransmissionModel'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.message_transmission_models.' + message_transmission_model_name).model
        else:
            message_transmission_model = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.message_transmission_models.{message_transmission_model_arg}').model

        return message_transmission_model

    @staticmethod
    def find_mobility_model(mobility_model_arg: str) -> Type['AbcMobilityModel']:
        """(static) Finds the mobility model.

        Parameters
        ----------
        mobility_model_arg : str
            The mobility model to find, specified as either:
            - "project_name:model_name" format to import from the project's mobility models.
            - "model_name" to import from the default mobility models.

        Returns
        -------
        Type[AbcMobilityModel]
            The mobility model class.
        """

        if (mobility_model_arg.__contains__(':')):
            project_name, mobility_model_name = mobility_model_arg.split(':')

            mobility_model: Type['AbcMobilityModel'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.mobility_models.' + mobility_model_name).model
        else:
            mobility_model = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.mobility_models.{mobility_model_arg}').model

        return mobility_model

    @staticmethod
    def find_connectivity_model(connectivity_model_arg: str) -> Type['AbcConnectivityModel']:
        """(static) Finds the connectivity model.

        Parameters
        ----------
        connectivity_model_arg : str
            The connectivity model to find, specified as either:
            - "project_name:model_name" format to import from the project's connectivity models.
            - "model_name" to import from the default connectivity models.

        Returns
        -------
        Type[AbcConnectivityModel]
            The connectivity model class.
        """

        if (connectivity_model_arg.__contains__(':')):
            project_name, connectivity_model_name = connectivity_model_arg.split(
                ':')

            connectivity_model: Type['AbcConnectivityModel'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.connectivity_models.' + connectivity_model_name).model
        else:
            connectivity_model = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.connectivity_models.{connectivity_model_arg}').model

        return connectivity_model

    @staticmethod
    def find_interference_model(interference_model_arg: str) -> Type['AbcInterferenceModel']:
        """(static) Finds the interference model.

        Parameters
        ----------
        interference_model_arg : str
            The interference model to find, specified as either:
            - "project_name:model_name" format to import from the project's interference models.
            - "model_name" to import from the default interference models.

        Returns
        -------
        Type[AbcInterferenceModel]
            The interference model class.
        """
        if (interference_model_arg.__contains__(':')):
            project_name, interference_model_name = interference_model_arg.split(
                ':')

            interference_model: Type['AbcInterferenceModel'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.interference_models.' + interference_model_name).model
        else:
            interference_model = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.interference_models.{interference_model_arg}').model

        return interference_model

    @staticmethod
    def find_reliability_model(reliability_model_arg: str) -> Type['AbcReliabilityModel']:
        """
        (static) Finds the reliability model.

        Parameters
        ----------
        reliability_model_arg : str
            The reliability model to find, specified as either:
            - "project_name:model_name" format to import from the project's reliability models.
            - "model_name" to import from the default reliability models.

        Returns
        -------
        Type[AbcReliabilityModel]
            The reliability model class.
        """

        if (reliability_model_arg.__contains__(':')):
            project_name, reliability_model_name = reliability_model_arg.split(
                ':')

            reliability_model: Type['AbcReliabilityModel'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.reliability_models.' + reliability_model_name).model
        else:
            reliability_model = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.reliability_models.{reliability_model_arg}').model

        return reliability_model

    @staticmethod
    def find_distribution_model(distribution_model_arg: str) -> Type['AbcDistributionModel']:
        """
        (static) Finds the distribution model.

        Parameters
        ----------
        distribution_model_arg : str
            The distribution model to find, specified as either:
            - "project_name:model_name" format to import from the project's distribution models.
            - "model_name" to import from the default distribution models.

        Returns
        -------
        Type[AbcDistributionModel]
            The distribution model class.
        """
        if (distribution_model_arg.__contains__(':')):
            project_name, distribution_model_name = distribution_model_arg.split(
                ':')

            distribution_model: Type['AbcDistributionModel'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.distribution_models.' + distribution_model_name).model
        else:
            distribution_model = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.distribution_models.{distribution_model_arg}').model

        return distribution_model

    @staticmethod
    def find_node_implementation(node_arg: str) -> Type['AbcNode']:
        """
        (static) Finds the node implementation.

        Parameters
        ----------
        node_arg : str
            The node implementation to find, specified as either:
            - "project_name:implementation_name" format to import from the project's nodes.
            - "implementation_name" to import from the default nodes.

        Returns
        -------
        Type[AbcNode]
            The node implementation class.
        """
        if (node_arg.__contains__(':')):
            project_name, node_name = node_arg.split(':')

            node_implementation: Type['AbcNode'] = importlib.import_module(
                SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.nodes.' + node_name).node
        else:
            node_implementation = importlib.import_module(
                f'apps.mobsinet.simulator.defaults.nodes.{node_arg}').node

        return node_implementation
