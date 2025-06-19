from abc import ABC, abstractmethod
from copy import deepcopy
from typing import TypedDict
from ..configuration.layout.form_section import FormSubSection


class AbcModelParameters(TypedDict):
    pass


class AbcModel(ABC):
    form_subsection_layout: FormSubSection

    def __init__(self, parameters: AbcModelParameters):
        self.parameters = parameters

    def __str__(self):
        return f'{self.__class__.__name__}'

    def clone(self):
        return deepcopy(self)

    @abstractmethod
    def check_parameters(self, parameters: AbcModelParameters) -> bool:
        """
        Validate the provided parameters for the model.

        This method checks if the given parameters meet the required
        criteria for the model. It should be implemented by subclasses
        to enforce specific parameter validation logic.

        Parameters
        ----------
        parameters : AbcModelParameters
            A dictionary containing parameter names and their values.

        Returns
        -------
        bool
            `True` if the parameters are valid, `False` otherwise.
        """

    @abstractmethod
    def set_parameters(self, parameters: AbcModelParameters) -> None:
        """
        Set the parameters for the model.

        This method updates the model with the provided parameters. It should be
        implemented by subclasses to apply specific parameter settings according
        to the model's requirements.

        Parameters
        ----------
        parameters : AbcModelParameters
            A dictionary containing parameter names and their values.
        """
