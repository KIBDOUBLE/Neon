import os

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

    if d[0] == "file":
        next = d[1].split()[0]
        path = v[1]
        if next == "read":
            result = open(path, 'r', encoding="utf-8").read()
        elif next == "write":
            open(path, 'w').write(cls.execute_line(line[len(v[0])+len(v[1])+2:], context, line_index, code, types).result)
        elif next == "delete":
            os.remove(path)

    else:
        p_result = False

    return PackageResult(ExecutionResult(result, context, types, Command(command, command_value)), p_result)
