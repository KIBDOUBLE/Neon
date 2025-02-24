from neon_parser import NeonParser
from new_types.command import Command
from new_types.execution_result import ExecutionResult
from new_types.line_list import LineList
from new_types.neon_type import NeonType
from new_types.package_result import PackageResult
from new_types.type_context import TypeContext
from variables.variables import Variables


# Тело пакета
def get(cls: NeonParser, line: str, context: Variables, line_index: int, code: LineList, types: TypeContext) -> PackageResult:
    result = ""
    p_result = True
    command = 0
    command_value = ""

    return PackageResult(ExecutionResult(result, context, types, Command(command, command_value)), p_result)


# Возможность добавлять новые типы переменных
def types() -> TypeContext:
    context = TypeContext()

    context.register(NeonType("type_name", lambda value: "check condition"))

    return context