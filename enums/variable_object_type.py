from enum import Enum


class VariableObjectType(Enum):
    Function = 0,
    Variable = 1,
    Package = 2,
    Empty = 3


def to_string(obj_type) -> str:
    type = int(obj_type)
    if type == 0: return "function"
    elif type == 1: return "variable"
    elif type == 2: return "package"
    else: return "empty"