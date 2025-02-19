import colorama

import line_list
from execution_result import ExecutionResult
from function import Function
from line_list import LineList
from variable import Variable
from variable_object import VariableObject
from variable_object_type import VariableObjectType
from variables import Variables
from colorama import Fore
colorama.init()


class Parser:
    slots = ["code", "variables"]
    def __init__(self, code: str):
        self.code: LineList = line_list.create(code)
        self.variables = Variables()
        self.currentLineIndex = 0

    def execute(self):
        self.__reader(self.code, self.variables)

    def __reader(self, code: LineList, context: Variables):
        req_skips = 0
        skips = 0
        current_line_index = 0
        for line in code.lines:
            if skips < req_skips:
                skips += 1
                continue
            else:
                current_line_index += req_skips
                skips = 0
                req_skips = 0

            result = self.execute_line(line, context, current_line_index, code)

            if result.contains_result():
                cmd = result.result.split(' ')
                if len(cmd) == 2:
                    if cmd[0] == "skip":
                        req_skips = int(cmd[1])

            current_line_index += 1
            context = result.variables

    @property
    def reader(self) -> None: return None

    @classmethod
    def execute_line(cls, line: str, context: Variables, line_index: int, code: LineList) -> ExecutionResult:
        v = line.split()
        result = ""

        def arg_at_is(index: int, value: str, in_v: bool=True) -> bool:
            if in_v:
                return v[index] == value
            else:
                return line[index] == value

        if arg_at_is(0, "~", False):
            result = eval(line.replace("~", "", 1))
        elif arg_at_is(0, "log"):
            print(cls.execute_line(line[4:], context, line_index, code).result)
        elif arg_at_is(0, "var"):
            value = v[2]
            can_add = v[1].endswith("<-") or v[2].startswith("<-")
            if value == "<-": value = v[3]
            if value.startswith("<-"): value = value[2:]
            if can_add: context.append(VariableObject(Variable(v[1], value), VariableObjectType.Variable))
            else: Parser.drop_exception(f"Missing '<-' in variable assignation! At {code.get_line(line_index)}")
        elif arg_at_is(0, "function"):
            name = v[1]
            context.append(VariableObject(Function(name, LineList([]), LineList([])), VariableObjectType.Function))
        elif context.is_variable(v[0]):
            variable = context.get(v[0]).get_if_variable()
            function = context.get(v[0]).get_if_function()
            if len(v) == 1:
                if variable: result = variable.value
                elif function:
                    pass
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

        return ExecutionResult(result, context)

    @classmethod
    def drop_exception(cls, message: str) -> None: print(Fore.RED + message + Fore.RESET)
