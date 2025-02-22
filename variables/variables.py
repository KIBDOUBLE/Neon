from tool import is_in, assign_variable_object_type
from variables.variable_object import VariableObject


class Variables:
    slots = ["__variables", "__number"]
    def __init__(self, number = 0):
        self.__variables = []
        self.__number = number

    @property
    def variables(self) -> None: return None

    @property
    def context(self) -> str:
        result = ""
        for variable_obj in self.__variables:
            variable_obj: VariableObject
            name = variable_obj.get_variable_name()
            result += f"{name}:{assign_variable_object_type(variable_obj).name};"
        return result

    @property
    def number(self) -> int: return self.__number

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
