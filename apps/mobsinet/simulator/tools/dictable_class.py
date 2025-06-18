import json
from typing import Any


class DictableClass:
    @classmethod
    def load_from_file(cls, file: str):
        with open(file, 'r') as f:
            config_data: dict = json.load(f)

        cls.load_from_dict(config_data)

    @classmethod
    def load_from_dict(cls, config_data: dict[str, Any]):
        for key, value in config_data.items():
            if key in cls.__dict__ and not key.startswith("__") and not callable(value):
                setattr(cls, key, value)

    @classmethod
    def to_dict(cls):
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and not callable(value)
        }
