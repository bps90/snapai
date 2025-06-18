import json
from typing import TYPE_CHECKING
from ..tools.dictable_class import DictableClass
from abc import abstractmethod

if TYPE_CHECKING:
    from .layout.form_layout import FormLayout


class BaseConfig(DictableClass):

    @classmethod
    def load_from_file(cls, config_file: str):
        """
        Loads configuration data from a file and updates the simulation configuration parameters accordingly.

        Parameters
        ----------
        config_file : str
            The file path of the configuration file.
        """
        return super().load_from_file(config_file)

    @classmethod
    @abstractmethod
    def get_form_layout(cls) -> 'FormLayout':
        pass
