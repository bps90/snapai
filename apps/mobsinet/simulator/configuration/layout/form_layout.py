from .form_section import FormSection, FormSubSection, FormSectionLine, FormSectionTextField, FormSectionFieldInformative
from typing import TYPE_CHECKING, Literal
from ...tools.dictable_class import DictableClass

if TYPE_CHECKING:
    from ..base_config import BaseConfig


class FormLayout(DictableClass):
    def __init__(self, config_class: type['BaseConfig']):
        self.sections: list[FormSection] = []
        self.config_class = config_class

    def to_dict(self):
        return {
            'sections': [section.to_dict() for section in self.sections]
        }

    def add_model_section(self, model_type: Literal['connectivity', 'mobility', 'interference', 'reliability', 'distribution', 'message_transmission']):
        return self.add_section(
            FormSection(
                id=f'{model_type}_model_section',
                title=f'{' '.join(model_type.split("_")).capitalize()} Model Parameters'
            ).add_subsections([
                FormSubSection(
                    id=f"{model_type}_model_subsection",
                ).add_line(
                    FormSectionLine().add_field(
                        FormSectionTextField(
                            id=f"{model_type}_model_name",
                            label=f"{' '.join(model_type.split("_")).capitalize()} Model",
                            name=f"{model_type}_model",
                            occuped_columns=12,
                            required=True,
                            informative=FormSectionFieldInformative(
                                title=f"The name of the {' '.join(model_type.split('_'))} model.",
                                help_text=f"The name of the {' '.join(model_type.split('_'))} model.<br/>Use the following format: \"project_name:model_name\" to import from the project's {' '.join(model_type.split('_'))} models.<br/>Use the following format: \"model_name\" to import from the default {' '.join(model_type.split('_'))} models.",
                                as_html=True
                            )
                        )
                    )
                ),
            ]).add_model_subsection(
                model=self.config_class.to_dict()[f'{model_type}_model'],
                model_type=model_type
            )
        )

    def add_model_sections(self, model_types: list[Literal['connectivity', 'mobility', 'interference', 'reliability', 'distribution', 'message_transmission']]):
        for model_type in model_types:
            self.add_model_section(model_type)

        return self

    def add_section(self, section: FormSection):
        for subsection in section.subsections:
            if (isinstance(subsection, FormSubSection)):
                for line in subsection.lines:
                    for field in line.fields:
                        field.init(self.config_class)

        self.sections.append(section)
        return self

    def add_sections(self, sections: list[FormSection]):
        for section in sections:
            self.add_section(section)
        return self
