from new_types.command import Command
from new_types.execution_result import ExecutionResult
from new_types.line_list import LineList
from new_types.package_result import PackageResult
from parser import Parser
from variables.variables import Variables


def get(cls: Parser, line: str, context: Variables, line_index: int, code: LineList) -> PackageResult:
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
            open(path, 'w').write(cls.execute_line(line[len(v[0])+len(v[1])+2:], context, line_index, code).result)

    else:
        p_result = False

    return PackageResult(ExecutionResult(result, context, Command(command, command_value)), p_result)
