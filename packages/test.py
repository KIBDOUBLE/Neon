from new_types.command import Command
from new_types.execution_result import ExecutionResult
from new_types.line_list import LineList
from new_types.package_result import PackageResult
from variables.variables import Variables


def get(line: str, context: Variables, line_index: int, code: LineList) -> PackageResult:
    result = ""
    p_result = True
    command = 0
    command_value = ""

    v = line.split(" ")

    if v[0] == "lol":
        result = "lol"
    else:
        p_result = False

    return PackageResult(ExecutionResult(result, context, Command(command, command_value)), p_result)