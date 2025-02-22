from enum import Enum


class VariableType(Enum):
    Integer = 0,
    String = 1,
    Boolean = 2,
    Unknown = 3,
    Operator = 4