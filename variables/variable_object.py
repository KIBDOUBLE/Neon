from variables.function import Function
from variables.package import Package
from variables.variable import Variable
from enums.variable_object_type import VariableObjectType


class VariableObject:
    slots = ["variables", "__type"]
    def __init__(self, variable, type: VariableObjectType):
        self.variable = variable
        self.__type = type

    @property
    def type(self) -> None: return None

    @classmethod
    def get_empty(cls): return VariableObject(None, VariableObjectType.Empty)

    def get_variable_name(self) -> str:
        if self.type_is(VariableObjectType.Variable):
            self.variable: Variable
            return self.variable.name
        elif self.type_is(VariableObjectType.Function):
            self.variable: Function
            return self.variable.name
        elif self.type_is(VariableObjectType.Package):
            self.variable: Package
            return self.variable.name
        else:
            return "NONE"

    def type_is(self, type: VariableObjectType) -> bool: return self.__type == type

    def get_if_variable(self) -> Variable:
        if self.type_is(VariableObjectType.Variable):
            return self.variable

    def get_if_function(self) -> Function:
        if self.type_is(VariableObjectType.Function):
            return self.variable

    def get_if_package(self) -> Package:
        if self.type_is(VariableObjectType.Package):
            return self.variable

    def is_empty(self) -> bool: return (self.variable is None) and (self.type_is(VariableObjectType.Empty))
