from typing import Any
from ...configuration.base_config import BaseConfig


class ProjectConfig(BaseConfig):
    connectivity_model = 'sample9:s9_connectivity'
    connectivity_model_parameters: dict[str, Any] = {}
    reliability_model = 'reliable_delivery'
    reliability_model_parameters: dict[str, Any] = {}
    interference_model = 'no_interference'
    interference_model_parameters: dict[str, Any] = {}
