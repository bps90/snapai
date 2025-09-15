from typing import TYPE_CHECKING, Literal, Any, cast
from abc import ABC, abstractmethod
import re

if TYPE_CHECKING:
    from ..base_config import BaseConfig


class FormSectionFieldInformative:
    def __init__(self,
                 title: str,
                 help_text: str | None = None,
                 as_html: bool = False):
        self.title = title
        self.help_text = help_text or title
        self.as_html = as_html

    def to_dict(self):
        return {
            'title': self.title,
            'help_text': self.help_text,
            'as_html': self.as_html
        }


class FormSectionField(ABC):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 nested_paths: list[str] = []
                 ):
        self.id = id
        self.label = label
        self.name = name
        self.occuped_columns = occuped_columns
        self.required = required
        self.informative = informative
        self.nested_paths: list[str] = nested_paths
        
    def add_nested_path(self, path: str):
        self.nested_paths.append(path)
        return self
    
    def set_nested_paths(self, paths: list[str]):
        self.nested_paths = paths
        return self

    @abstractmethod
    def init(self, config_class: type['BaseConfig']):
        """Called by form layout to initialize the field"""
        pass

    @abstractmethod
    def to_dict(self):
        pass


class FormSectionTextField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 min_length: int = 0,
                 max_length: int | None = None
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.min_length = min_length
        self.max_length = max_length
        self.value: str | None = None

    def init(self, config_class):
        working_config = config_class.to_dict()
        
        for path in self.nested_paths:
            working_config = working_config[path]
        
        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value = working_config[self.name]
        if value is None and self.required:
            raise Exception(f"Field {self.name} is required")

        if value is not None and not isinstance(value, str):
            raise Exception(f"Field {self.name} is not a string")
        
        if value is not None and len(value) < self.min_length:
            raise Exception(f"Field {self.name} is too short")

        if value is not None and self.max_length is not None and len(value) > self.max_length:
            raise Exception(f"Field {self.name} is too long")

        self.value = value
        return self

    def to_dict(self):
        return {
            'type': 'text',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths,
            'min_length': self.min_length,
            'max_length': self.max_length
        }


class FormSectionNumberField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 is_float: bool = False,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 min_value: float | int | None = None,
                 max_value: float | int | None = None,
                 is_angle: Literal['rad', 'deg', False] = False
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.is_float: bool = is_float
        self.min_value = min_value
        self.max_value = max_value
        self.is_angle = is_angle
        self.value: float | int | None = None

    def init(self, config_class):
        working_config = config_class.to_dict()

        for path in self.nested_paths:
            working_config = working_config[path]
            
        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value = working_config[self.name]

        if value is None and self.required:
            raise Exception(f"Field {self.name} is required")

        if value is not None and not isinstance(value, (int, float)):
            raise Exception(f"Field {self.name} is not a number")

        if not self.is_float and (not isinstance(value, int) or value is not None):
            raise Exception(f"Field {self.name} is not an int")
        
        if value is not None and self.min_value is not None and value < self.min_value:
            raise Exception(f"Field {self.name} is too small")

        if value is not None and self.max_value is not None and value > self.max_value:
            raise Exception(f"Field {self.name} is too big")

        self.value = value
        return self

    def to_dict(self):
        return {
            'type': 'number',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'is_float': self.is_float,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'is_angle': self.is_angle
        }


class FormSectionPercentageField(FormSectionNumberField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 is_float: bool = False,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 ):
        super().__init__(id, label, name, occuped_columns, is_float, required, informative, 0, 100)
    
    def to_dict(self):
        return {
            **super().to_dict(),
            'type': 'percentage',
        }


class FormSectionSelectField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 options: list[dict[Literal['value', 'label'], Any]],
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.options = options
        self.value: Any = None

    def init(self, config_class):
        working_config = config_class.to_dict()

        for path in self.nested_paths:
            working_config = working_config[path]
        
        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value = working_config[self.name]

        if (value is None and self.required):
            raise Exception(f"Field {self.name} is required")

        if (value is not None and value not in [option['value'] for option in self.options]):
            raise Exception(
                f"Field {self.name} value {value} not found in options")

        self.value = value
        return self

    def to_dict(self):
        return {
            'type': 'select',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'options': self.options,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths
        }
        
class FormSectionModelSelectField(FormSectionSelectField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 model_type: Literal['connectivity', 'mobility', 'interference', 'reliability', 'distribution', 'message_transmission'],
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None):
        from ...tools.models_search_engine import ModelsSearchEngine
        options = cast(list[dict[Literal['value', 'label'], Any]], [({ 'value': model, 'label': model }) for model in ModelsSearchEngine.get_models_names(model_type)])
        super().__init__(id, label, name, occuped_columns, options, required, informative)
        self.model_type = model_type

    def to_dict(self):
        return {
            **super().to_dict(),
            'type': 'model_select',
            'model_type': self.model_type        
        }

class FormSectionMultiSelectField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 options: list[dict[Literal['value', 'label'], Any]],
                 min_selected: int = 0,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 max_selected: int | None = None
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.options = options
        self.min_selected = min_selected
        self.max_selected = max_selected
        self.value: list[Any] = []

    def to_dict(self):
        return {
            'type': 'multiselect',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'options': self.options,
            'min_selected': self.min_selected,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths,
            'max_selected': self.max_selected
        }

    def init(self, config_class):
        working_config = config_class.to_dict()

        for path in self.nested_paths:
            working_config = working_config[path]
        
        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value: list[Any] = working_config[self.name]

        if (len(value) < self.min_selected):
            raise Exception(
                f"Field {self.name} must have at least {self.min_selected} selected")

        for v in value:
            if (v not in [option['value'] for option in self.options]):
                raise Exception(
                    f"Field {self.name} value {v} not found in options")

        if (self.max_selected is not None and len(value) > self.max_selected):
            raise Exception(
                f"Field {self.name} must have at most {self.max_selected} selected")

        self.value = value
        return self


class FormSectionCheckboxField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 required: bool = False,
                 informative: FormSectionFieldInformative | None = None
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.value: bool | None = None

    def to_dict(self):
        return {
            'type': 'checkbox',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths
        }

    def init(self, config_class):
        working_config = config_class.to_dict()

        for path in self.nested_paths:
            working_config = working_config[path]
        
        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value = working_config[self.name]
        if value is None and self.required:
            raise Exception(f"Field {self.name} is required")

        if value is not None and not isinstance(value, bool):
            raise Exception(f"Field {self.name} is not a boolean")

        self.value = value
        return self


class FormSectionNumberPairField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 is_float: bool = False,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 min_left_value: float | int | None = None,
                 max_left_value: float | int | None = None,
                 min_right_value: float | int | None = None,
                 max_right_value: float | int | None = None,
                 right_should_be_gte_left: bool = False,
                 is_angle: Literal['rad', 'deg', False] = False
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.is_float: bool = is_float
        self.min_left_value = min_left_value
        self.max_left_value = max_left_value
        self.min_right_value = min_right_value
        self.max_right_value = max_right_value
        self.right_should_be_gte_left = right_should_be_gte_left
        self.is_angle = is_angle
        self.value: list[float | int] | None = None

    def to_dict(self):
        return {
            'type': 'number_pair',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'is_float': self.is_float,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths,
            'min_left_value': self.min_left_value,
            'max_left_value': self.max_left_value,
            'min_right_value': self.min_right_value,
            'max_right_value': self.max_right_value,
            'right_should_be_gte_left': self.right_should_be_gte_left,
            'is_angle': self.is_angle
        }

    def init(self, config_class):
        working_config = config_class.to_dict()

        for path in self.nested_paths:
            working_config = working_config[path]
        
        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value = working_config[self.name]

        if value is None and self.required:
            raise Exception(f"Field {self.name} is required")

        if value is not None and not isinstance(value, list):
            raise Exception(f"Field {self.name} is not a list")

        if (value is not None):
            for v in value:
                if (not isinstance(v, (int, float))):
                    raise Exception(f"Field {self.name} is not a number")

                if not self.is_float and not isinstance(v, int):
                    raise Exception(f"Field {self.name} is not an int")
                
            if (self.min_left_value is not None and value[0] < self.min_left_value):
                raise Exception(f"Field {self.name} left value is too small")

            if (self.max_left_value is not None and value[0] > self.max_left_value):
                raise Exception(f"Field {self.name} left value is too big")

            if (self.min_right_value is not None and value[1] < self.min_right_value):
                raise Exception(f"Field {self.name} right value is too small")

            if (self.max_right_value is not None and value[1] > self.max_right_value):
                raise Exception(f"Field {self.name} right value is too big")

            if (self.right_should_be_gte_left and value[1] < value[0]):
                raise Exception(f"Field {self.name} right value should be greater than or equal to left value")
            
        self.value = value
        return self


class FormSectionColorField(FormSectionField):
    def __init__(self,
                 id: str,
                 label: str,
                 name: str,
                 occuped_columns: int,
                 required: bool = True,
                 informative: FormSectionFieldInformative | None = None,
                 ):
        super().__init__(id, label, name, occuped_columns, required, informative)
        self.value: str | None = None

    def init(self, config_class):
        working_config = config_class.to_dict()

        for path in self.nested_paths:
            working_config = working_config[path]

        if self.name not in working_config:
            raise Exception(f"Field {self.name} not found in config class")

        value = working_config[self.name]
        if value is None and self.required:
            raise Exception(f"Field {self.name} is required")

        if value is not None and not isinstance(value, str):
            raise Exception(f"Field {self.name} is not a string")
    
        if value is not None and not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            raise Exception(f"Field {self.name} is not a valid hex color")

        self.value = value
        return self

    def to_dict(self):
        return {
            'type': 'color',
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'occuped_columns': self.occuped_columns,
            'required': self.required,
            'informative': self.informative.to_dict() if self.informative else None,
            'value': self.value,
            'nested_paths': self.nested_paths,
        }

class FormSectionLine:
    def __init__(self):
        self.__occuped_columns = 0
        self.fields: list[FormSectionField] = []

    def add_field(self, field: FormSectionField):
        self.__occuped_columns += field.occuped_columns

        if self.__occuped_columns > 12:
            raise Exception("FormSectionLine has more than 12 columns")

        self.fields.append(field)
        return self

    def add_fields(self, fields: list[FormSectionField]):
        occuped_columns = self.__occuped_columns

        for field in fields:
            occuped_columns += field.occuped_columns

            if occuped_columns > 12:
                raise Exception("FormSectionLine has more than 12 columns")

        for field in fields:
            self.add_field(field)
        return self

    def to_dict(self):
        return {
            'fields': [field.to_dict() for field in self.fields]
        }


class FormSubSection:
    def __init__(self, id: str, title: str | None = None, model: bool = False):
        self.id = id
        self.title = title
        self.model_parameters: bool = model
        self.lines: list[FormSectionLine] = []
        self._nested_paths: list[str] = []

    def add_line(self, line: FormSectionLine):
        for path in self._nested_paths:
            for field in line.fields:
                field.add_nested_path(path)
        
        self.lines.append(line)
        return self

    def add_lines(self, lines: list[FormSectionLine]):
        for line in lines:
            self.add_line(line)
        return self

    def add_nested_path(self, path: str):
        self._nested_paths.append(path)
        self.__update_fields_nested_paths()
        return self
    
    def set_nested_paths(self, paths: list[str]):
        self._nested_paths = paths
        self.__update_fields_nested_paths()
        return self

    def __update_fields_nested_paths(self):
        for line in self.lines:
            for field in line.fields:
                field.set_nested_paths(self._nested_paths)
        return self
    
    def set_model_parameters(self, model_parameters: bool):
        self.model_parameters = model_parameters
        return self
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'lines': [line.to_dict() for line in self.lines],
            'model_parameters': self.model_parameters
        }

class FormSection:
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title
        self.subsections: list[FormSubSection] = []

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subsections': [subsection.to_dict() for subsection in self.subsections]
        }

    def add_subsection(self, subsection: FormSubSection):
        self.subsections.append(subsection)
        return self

    def add_subsections(self, subsections: list[FormSubSection]):
        for subsection in subsections:
            self.add_subsection(subsection)
        return self

    

class FormModelSection(FormSection):
    def __init__(self, id: str, title: str, model: str, model_type: Literal['connectivity', 'mobility', 'interference', 'reliability', 'distribution', 'message_transmission']):
        super().__init__(id, title)
        self.model = model
        self.model_type = model_type
        
    def to_dict(self):
        return {
            **super().to_dict(),
            'model': self.model,
            'model_type': self.model_type
        }
        
    def add_parameters_subsection(self):
        from ...tools.models_search_engine import ModelsSearchEngine
        Model = ModelsSearchEngine.find_model(self.model, self.model_type)
        
        return self.add_subsection(
            (Model.form_subsection_layout if 'form_subsection_layout' in Model.__dict__ else FormSubSection(
            id=f"{self.model.replace(':', '_')}_parameters_subsection"
        )).set_model_parameters(True).set_nested_paths([f'{self.model_type}_model_parameters']))