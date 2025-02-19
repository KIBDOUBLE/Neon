from string_operations import is_in
from variable_object import VariableObject
from variable_object_type import VariableObjectType


class Variables:
    slots = ["__variables"]
    def __init__(self):
        self.__variables = []

    @property
    def variables(self) -> None: return None

    def append(self, variable: VariableObject) -> None:
        for variable2 in self.__variables:
            variable2: VariableObject
            if variable2.get_variable_name() == variable.get_variable_name(): return
        self.__variables.append(variable)

    def delete(self, variable: VariableObject) -> None: self.__variables.remove(variable)

    def get(self, name: str) -> VariableObject:
        for variable in self.__variables:
            variable: VariableObject
            if variable.get_variable_name() == name:
                return variable
        return VariableObject.get_empty()

    def get_python_pattern(self):
        code = ""
        for variableObj in self.__variables:
            variableObj: VariableObject
            variable = variableObj.get_if_variable()
            if variable:
                code += f"{variable.name} = {variable.value}\n"
        return code

    def is_variable(self, data: str) -> bool:
        if is_in(data, "\""): return False
        elif not self.get(data).is_empty(): return True
        return False
