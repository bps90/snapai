from typing import Any
from ...configuration.base_project_config import BaseProjectConfig
from ...configuration.layout.form_layout import FormLayout
import json
import os
from ...configuration.sim_config import SimulationConfig
from ...configuration.layout.form_section import FormSection, FormSubSection, FormSectionLine, FormSectionMultiSelectField, FormSectionFieldInformative, FormSectionSelectField, FormSectionNumberPairField

class ProjectConfig(BaseProjectConfig):
    connectivity_model: str = ''
    connectivity_model_parameters: dict[str, Any] = {}
    reliability_model: str = ''
    reliability_model_parameters: dict[str, Any] = {}
    interference_model: str = ''
    interference_model_parameters: dict[str, Any] = {}
    number_pair_test: list[int] = [0,40]
    multiselect_test: list[int] = [0,1]
    multiselect_test2: list[str] = ['a', 'b']
    select_test: int = 0
    select_test2: str = 'a'

    @classmethod
    def get_form_layout(cls) -> FormLayout:
        return FormLayout(config_class=ProjectConfig).add_model_sections([
            'connectivity',
            'reliability',
            'interference'
        ]).add_section(FormSection(
            id="test1",
            title="Test 1"
        ).add_subsection(
            FormSubSection(
                id="test1-subsection",
                title="Test 1 Subsection"
            ).add_line(
                FormSectionLine().add_fields([
                    FormSectionNumberPairField(
                        id="number_pair_test",
                        label="Number Pair Test",
                        name="number_pair_test",
                        occuped_columns=6,
                        is_float=False,
                        required=True,
                        informative=FormSectionFieldInformative(
                            title="Number Pair Test Informative"
                        ),
                        min_left_value=0,
                        max_left_value=50,
                        min_right_value=20,
                        max_right_value=100
                    ),
                    FormSectionMultiSelectField(
                        id="multiselect_test",
                        label="Multiselect Test",
                        name="multiselect_test",
                        occuped_columns=3,
                        required=True,
                        informative=FormSectionFieldInformative(
                            title="Multiselect Test Informative"
                        ),
                        options=[
                            {
                                'label': 'Option 1',
                                'value': 0
                            },
                            {
                                'label': 'Option 2',
                                'value': 1
                            },
                            {
                                'label': 'Option 3',
                                'value': 2
                            },
                            {
                                'label': 'Option 4',
                                'value': 3
                            }
                        ]
                    ),
                    FormSectionMultiSelectField(
                        id="multiselect_test2",
                        label="Multiselect Test 2",
                        name="multiselect_test2",
                        occuped_columns=3,
                        required=True,
                        informative=FormSectionFieldInformative(
                            title="Multiselect Test 2 Informative"
                        ),
                        options=[
                            {
                                'label': 'Option A',
                                'value': 'a'
                            },
                            {
                                'label': 'Option B',
                                'value': 'b'
                            },
                            {
                                'label': 'Option C',
                                'value': 'c'
                            },
                            {
                                'label': 'Option D',
                                'value': 'd'
                            }
                        ]
                    ),
                ])
            ).add_line(FormSectionLine().add_fields([
                FormSectionSelectField(
                    id="select_test",
                    label="Select Test",
                    name="select_test",
                    occuped_columns=3,
                    required=True,
                    informative=FormSectionFieldInformative(
                        title="Select Test Informative"
                    ),
                    options=[
                        {
                            'label': 'Option 1',
                            'value': 0
                        },
                        {
                            'label': 'Option 2',
                            'value': 1
                        },
                        {
                            'label': 'Option 3',
                            'value': 2
                        },
                        {
                            'label': 'Option 4',
                            'value': 3
                        }
                    ]
                     
                ),
                FormSectionSelectField(
                    id="select_test2",
                    label="Select Test 2",
                    name="select_test2",
                    occuped_columns=6,
                    required=True,
                    informative=FormSectionFieldInformative(
                        title="Select Test 2 Informative"
                    ),
                    options=[
                        {
                            'label': 'Option A',
                            'value': 'a'
                        },
                        {
                            'label': 'Option B',
                            'value': 'b'
                        },
                        {
                            'label': 'Option C',
                            'value': 'c'
                        },
                        {
                            'label': 'Option D',
                            'value': 'd'
                        }
                    ]
                )
            ]))
        ))


# Populate the ProjectConfig object
with open(os.path.join(SimulationConfig.PROJECTS_DIR, 'sample9', 'config.json'), 'r') as f:
    config_data = json.load(f)

    ProjectConfig.load_from_dict(config_data['project_config'])


if (__name__ == '__main__'):
    print(json.dumps(ProjectConfig.get_form_layout().to_dict(), indent=4))
