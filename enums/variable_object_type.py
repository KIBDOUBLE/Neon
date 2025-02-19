from enum import Enum


class VariableObjectType(Enum):
    Function = 0,
    Variable = 1,
    Empty = 2


def to_string(obj_type) -> str:
    type = int(obj_type)
    if type == 0: return "function"
    elif type == 1: return "variables"
    else: return "empty"