import colorama

from types import line_list
from types.command import Command
from types.execution_result import ExecutionResult
from variables.function import Function
from types.line_list import LineList
from tool import get_in, tab_clear
from variables.variable import Variable
from variables.variable_object import VariableObject
from enums.variable_object_type import VariableObjectType
from variables.variables import Variables
from colorama import Fore
from settings import CONFIG
colorama.init()


class Parser:
    slots = ["code", "variables"]
    def __init__(self, code: str):
        self.code: LineList = line_list.create(code)
        self.variables = Variables(0)

    def execute(self):
        self.__reader(self.code, self.variables)

    @classmethod
    def __reader(cls, code: LineList, context: Variables) -> ExecutionResult:
        if CONFIG.debug: print(f"<reader> context: {context.number} -> code={code.text}")
        req_skips = 0
        skips = 0
        current_line_index = 0
        to_return = ExecutionResult("", context, Command(0))
        for line in code.lines:
            line: str
            if skips < req_skips:
                skips += 1
                continue
            else:
                current_line_index += req_skips
                skips = 0
                req_skips = 0

            result = cls.execute_line(tab_clear(line), context, current_line_index, code)

            if result.command.command != 0:
                cmd = result.command
                if cmd.command == 10:
                    req_skips = int(cmd.i_value)
                elif cmd.command == 11:
                    to_return = ExecutionResult(result.result[7:], result.variables, Command(0))
                    break

            current_line_index += 1
            context = result.variables
        return to_return

    @property
    def reader(self) -> None: return None

    @classmethod
    def call_function(cls, function: Function, args: LineList, current_context: Variables, line_index: int, code: LineList) -> ExecutionResult:
        context = Variables(1)
        for i in range(args.length()):
            arg_name = function.req_args.get_line(i)
            if CONFIG.debug: print(f"New var in function: {arg_name}!")
            arg_value = cls.execute_line(args.get_line(i), current_context, line_index, code).result
            variable = Variable(arg_name, arg_value, Variable.get_type(arg_value))
            context.append(VariableObject(variable, VariableObjectType.Variable))
        result = cls.__reader(function.body, context)
        return result

    @classmethod
    def execute_line(cls, line: str, context: Variables, line_index: int, code: LineList) -> ExecutionResult:
        v = line.split()
        result = ""
        command = 0
        command_value = None

        def arg_at_is(index: int, value: str, in_v: bool=True) -> bool:
            if index >= len(v) or index >= len(line): return False
            if in_v:
                return v[index] == value
            else:
                return line[index] == value

        if len(v) == 0: return ExecutionResult(result, context, Command(0))

        if arg_at_is(0, "~", False):
            result = eval(line.replace("~", "", 1))

        elif arg_at_is(0, "log"):
            print(cls.execute_line(line[4:], context, line_index, code).result)

        elif arg_at_is(0, "var"):
            value = v[2]
            can_add = v[1].endswith("<-") or v[2].startswith("<-")

            if value == "<-": value = v[3]
            if value.startswith("<-"): value = value[2:]

            if can_add:
                variable = Variable(v[1], value, Variable.get_type(value))
                context.append(VariableObject(variable, VariableObjectType.Variable))
            else:
                Parser.drop_exception(f"Missing '<-' in variable assignation! At {code.get_line(line_index)}")

        elif arg_at_is(0, "function"):
            name = v[1]
            body = cls.get_body(line_index, code)
            args = v[3]
            can_continue = v[2] == "<-" or v[3].startswith("<-")
            if v[3].startswith("<-"): args = args[2:]
            if can_continue:
                function = Function(name, body, get_in(args))
                context.append(VariableObject(function, VariableObjectType.Function))
                command = 10
                command_value = function.body.length()

        elif arg_at_is(0, "return"): result = line[7:]

        elif context.is_variable(v[0]):
            variable = context.get(v[0]).get_if_variable()
            function = context.get(v[0]).get_if_function()

            if len(v) == 1:
                if variable:
                    result = variable.value
                    if CONFIG.debug: print(f"context: {context.number} -> {variable.name}={result}")
                elif function:
                    if function.req_args.length() == 0:
                        result = cls.call_function(function, LineList.empty(), context, line_index, code).result
            elif len(v) > 1:
                if variable:
                    if "<-" in line:
                        can_set = v[0].endswith("<-") or v[1].startswith("<-") or v[2].startswith("<-")
                        new_value = v[2]
                        if new_value.startswith("<-"): new_value = new_value.replace("<-", "", 1)
                        if can_set:
                            variable.value = new_value
                        else:
                            Parser.drop_exception(f"Missing '<-' in variable set! At {code.get_line(line_index)}")
                elif function:
                    args = v[1]
                    can_continue = v[1] == "->" or v[2].startswith("->")
                    if v[1] == "->": args = v[2]
                    if can_continue:
                        result = cls.call_function(function, get_in(args), context, line_index, code).result
        else: result = line

        execution_result = ExecutionResult(result, context, Command(command, command_value))
        if CONFIG.debug: print(f"<execute_line> context:{context.number} -> line={line} ; result={execution_result} ; \n     full context:\n{context.context}")
        return execution_result

    @classmethod
    def get_body(cls, init_index: int, code: LineList) -> LineList:
        lines = []
        i = init_index + 1
        while not "end" in code.get_line(i):
            lines.append(code.get_line(i))
            i += 1
        return LineList(lines)

    @classmethod
    def drop_exception(cls, message: str) -> None: print(Fore.RED + message + Fore.RESET)
