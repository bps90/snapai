from typing import Any
from ...configuration.base_project_config import BaseProjectConfig
from ...configuration.layout.form_layout import FormLayout
import json
import os
from ...configuration.sim_config import SimulationConfig


class ProjectConfig(BaseProjectConfig):
    connectivity_model: str = ''
    connectivity_model_parameters: dict[str, Any] = {}
    reliability_model: str = ''
    reliability_model_parameters: dict[str, Any] = {}
    interference_model: str = ''
    interference_model_parameters: dict[str, Any] = {}

    @classmethod
    def get_form_layout(cls) -> FormLayout:
        return FormLayout(config_class=ProjectConfig).add_model_sections([
            'connectivity',
            'reliability',
            'interference'
        ])


# Populate the ProjectConfig object
with open(os.path.join(SimulationConfig.PROJECTS_DIR, 'sample9', 'config.json'), 'r') as f:
    config_data = json.load(f)

    ProjectConfig.load_from_dict(config_data['project_config'])


if (__name__ == '__main__'):
    print(json.dumps(ProjectConfig.get_form_layout().to_dict(), indent=4))
