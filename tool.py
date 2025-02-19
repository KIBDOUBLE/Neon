from new_types.line_list import LineList
from variables.variable_object import VariableObject
from enums import variable_object_type


def is_in(string: str, border: str) -> bool:
    return string.startswith(border) and string.endswith(border)

def get_in(obj: str) -> LineList:
    obj = obj.replace(" ", "")
    obj = obj[:-1]
    obj = obj[1:]
    return LineList(obj.split(","))

def tab_clear(string: str) -> str:
    while string.startswith(" "): string = string[1:]
    return string

def assign_variable_object_type(variable: VariableObject) -> variable_object_type.VariableObjectType:
    if variable.get_if_variable(): return variable_object_type.VariableObjectType.Variable
    elif variable.get_if_function(): return variable_object_type.VariableObjectType.Function
    else: return variable_object_type.VariableObjectType.Empty
