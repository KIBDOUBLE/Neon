import tool

from new_types.neon_type import NeonType
from new_types.type_context import TypeContext


class Variable:
    slots = ["__name", "value", "__type"]
    def __init__(self, name: str, value, type: NeonType):
        self.__name = name
        self.value = value
        self.__type = type

    @property
    def name(self) -> str: return self.__name

    @property
    def type(self) -> str: return self.__type.name

    def type_is(self, type: NeonType) -> bool: return self.type == type.name

    @classmethod
    def get_type(cls, value, types: TypeContext) -> NeonType:
        for key in types.data:
            type: NeonType = types.get(key)
            if type.confirm(value):
                return type
        return types.get("unknown")

    @classmethod
    def get_type_is(cls, value, type: NeonType, types: TypeContext) -> bool: return cls.get_type(value, types).name == type.name

    @property
    def state(self) -> bool: return tool.string_to_bool(self.value)

    def edit_value(self, new_value: str, types: TypeContext) -> None:
        self.value = new_value
        self.__type = self.get_type(new_value, types)
