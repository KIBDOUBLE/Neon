from new_types.command import Command
from new_types.execution_result import ExecutionResult
from new_types.line_list import LineList
from new_types.package_result import PackageResult
from neon_parser import NeonParser
from new_types.type_context import TypeContext
from variables.variables import Variables


def get(cls: NeonParser, line: str, context: Variables, line_index: int, code: LineList, types: TypeContext) -> PackageResult:
    d = line.split(".")
    v = line.split()
    result = ""
    p_result = True
    command = 0
    command_value = ""

    if len(d) <= 1: return PackageResult(ExecutionResult("", context, types, Command(0)), False)

    if d[1] == "length":
        data = cls.execute_line(d[0], context, line_index, code, types).result
        result = f"{len(data)}"
    else:
        p_result = False

    return PackageResult(ExecutionResult(result, context, types, Command(command, command_value)), p_result)
