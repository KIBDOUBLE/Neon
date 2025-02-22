import tool
from enums.operators import Operators
from enums.variable_type import VariableType


class Variable:
    slots = ["__name", "value", "__type"]
    def __init__(self, name: str, value: str, type: VariableType):
        self.__name = name
        self.value = value
        self.__type = type

    @property
    def name(self) -> str: return self.__name

    @property
    def type(self) -> VariableType: return self.__type

    @property
    def is_digit(self) -> bool: return self.__type == VariableType.Integer

    @classmethod
    def get_type(cls, value: str) -> VariableType:
        if tool.is_in(value, "\""):
            return VariableType.String
        elif value == "false" or value == "true":
            return VariableType.Boolean
        elif value.isdigit():
            return VariableType.Integer
        elif value in Operators.all():
            return VariableType.Operator
        return VariableType.Unknown

    @property
    def state(self) -> bool: return tool.string_to_bool(self.value)

    def edit_value(self, new_value: str) -> None:
        self.value = new_value
        self.__type = self.get_type(new_value)
