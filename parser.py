import math
from collections.abc import ValuesView

import colorama

import tool
from enums.operators import Operators
from enums.variable_type import VariableType
from new_types import line_list
from new_types.command import Command
from new_types.execution_result import ExecutionResult
from variables.function import Function
from new_types.line_list import LineList
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
        if CONFIG.hello_message: print(f"Код {self.code.deep} был успешно запущен с входными аргументами {CONFIG.info()}\n")
        self.__reader(self.code, self.variables)
        self.drop_wait()

    @classmethod
    def __reader(cls, code: LineList, context: Variables) -> ExecutionResult:
        if CONFIG.debug and not CONFIG.only_return_results: print(f"<reader> context: {context.number} -> code={code.text}")
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
                    to_return = ExecutionResult(result.result, result.variables, Command(0))
                    break

            current_line_index += 1
            context = result.variables
        return to_return

    @property
    def reader(self) -> None: return None

    @classmethod
    def call_function(cls, function: Function, args: LineList, current_context: Variables, line_index: int, code: LineList) -> ExecutionResult:
        context = Variables(1)
        for i in range(args.length):
            arg_name = function.req_args.get_line(i)
            if CONFIG.debug and not CONFIG.only_return_results: print(f"New var in function: {arg_name}!")
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

        def explain_code(explain):
            if CONFIG.explain_mode:
                print(explain)

        def execute_here(line: str) -> ExecutionResult:
            return cls.execute_line(line, context, line_index, code)

        def arg_at_is(index: int, value: str, in_v: bool=True) -> bool:
            if index >= len(v) or index >= len(line): return False
            if in_v:
                return v[index] == value
            else:
                return line[index] == value

        if len(v) == 0: return ExecutionResult(result, context, Command(0))
        elif v[0].startswith(Operators.Ignore.get()): return ExecutionResult(result, context, Command(0))

        if line.startswith(Operators.End.get()): return ExecutionResult(result, context, Command(10, code.length))

        # Python operator
        if arg_at_is(0, Operators.Python.get(), False):
            try: result = eval(line[1:])
            except NameError as ExceptionName: cls.drop_exception(str(ExceptionName))

        # Expression operator
        elif arg_at_is(0, Operators.Expression.get(), False):
            expression = line[1:]
            python_expression = ""
            data = expression.split(" ")
            req_skips = 0
            skips = 0
            make_all_string = False
            index = 0
            for key in data:
                if skips < req_skips:
                    skips += 1
                    continue
                else:
                    req_skips = 0
                    skips = 0
                variable_obj = context.get(key)
                variable = variable_obj.get_if_variable()
                function = variable_obj.get_if_function()
                if not variable_obj.is_empty():
                    if variable:
                        value = variable.value
                        if variable.type == VariableType.String:
                            value = f"\"{value}\""
                        python_expression += f"{value}"
                    elif function:
                        python_expression += f"{execute_here(expression[len(python_expression):]).result}"
                        req_skips = 2
                else:
                    if key.startswith("\"") and not key.endswith("\""):
                        counter = 1
                        next_key = data[index+1]
                        keys = [key, next_key]
                        while not next_key.endswith("\""):
                            next_key = data[index + counter]
                            keys.append(next_key)
                            counter += 1
                        req_skips = counter
                        key = "`".join(keys)
                    if Variable.get_type(key) == VariableType.String: make_all_string = True
                    python_expression += key
                python_expression += " "
                index += 1
            data = python_expression.split(" ")
            if make_all_string:
                python_expression = ""
                for key in data:
                    key_type = Variable.get_type(key)
                    if key_type == VariableType.String:
                        python_expression += key
                    elif key_type == VariableType.Operator:
                        python_expression += key
                    else:
                        python_expression += f"\"{key}\""
                    python_expression += " "
            python_expression = python_expression.replace("`", " ")
            result = execute_here(f"~{python_expression}").result

        # Print operation
        elif arg_at_is(0, "log"):
            if not CONFIG.explain_mode: print(execute_here(line[4:]).result)
            explain_code(f"В строке '{line}' интерпретатор выполняет операцию по отображению '{line[4:]}'")
        elif arg_at_is(0, "forcelog"):
            print(execute_here(line[9:]).result)
            explain_code(f"В строке '{line}' интерпретатор выполняет операцию по отображению в любом случае '{line[4:]}'")

        elif arg_at_is(0, "if"):
            condition_variable = Variable("condition", "", VariableType.Unknown)
            arg = str(execute_here(line[3:]).result).lower()
            condition_variable.edit_value(arg)
            if condition_variable.type == VariableType.Boolean:
                body = cls.get_body(line_index, code)
                if not condition_variable.state:
                    command = 10
                    command_value = body.length
            else:
                Parser.drop_exception(f"Condition can't be not boolean type! At {code.get_line(line_index)}")

        # Variable add operation
        elif arg_at_is(0, "var"):
            can_add = v[1].endswith(Operators.Set.get()) or v[2].startswith(Operators.Set.get())

            remove_count = len(v[1]) + len(v[0])
            if v[1].endswith(Operators.Set.get()) or v[3].startswith(Operators.Set.get()):
                remove_count += 3
            elif v[2].startswith(Operators.Set.get()):
                remove_count += 5
            value = execute_here(line[remove_count:]).result

            if can_add:
                variable = Variable(v[1], value, Variable.get_type(str(value)))
                context.append(VariableObject(variable, VariableObjectType.Variable))
                explain_code(f"В строке '{line}' интерпретатор выполняет операцию по созданию переменной '{v[1]}' со значением {value}")
            else:
                Parser.drop_exception(f"Missing '{Operators.Set.get()}' in variable assignation! At {code.get_line(line_index)}")

        # Function add operation
        elif arg_at_is(0, "function"):
            name = v[1]
            body = cls.get_body(line_index, code)
            args = v[3]
            can_continue = v[2] == Operators.Set.get() or v[3].startswith(Operators.Set.get())
            if v[3].startswith(Operators.Set.get()): args = args[2:]
            if can_continue:
                function = Function(name, body, get_in(args))
                context.append(VariableObject(function, VariableObjectType.Function))
                explain_code(f"В строке '{line}' интерпретатор выполняет операцию по созданию функции '{v[1]}'")
                command = 10
                command_value = function.body.length

        # Return
        elif arg_at_is(0, "return"):
            result = execute_here(line[7:]).result
            if ExecutionResult.is_execution_result(result): result = ExecutionResult.restore(result).result
            explain_code(f"В строке '{line}' интерпретатор выполняет операцию по возвращению значения '{line[7:]}'")
            command = 11

        # User input
        elif arg_at_is(0, "input"):
            message = ""
            if len(v) > 1: message = execute_here(line[6:]).result
            explain_code(f"В строке '{line}' интерпретатор ожидает ввод пользователя")
            result = input(message)


        # Variables and functions operations
        elif context.is_variable(v[0]):
            variable = context.get(v[0]).get_if_variable()
            function = context.get(v[0]).get_if_function()

            if len(v) == 1:
                if variable:
                    result = variable.value
                    explain_code(f"В строке '{line}' интерпретатор выполняет операцию по поиску переменной с именем '{v[0]}'")
                    if CONFIG.debug and not CONFIG.only_return_results: print(f"context: {context.number} -> {variable.name}={result}")
                elif function:
                    if function.req_args.length == 0:
                        explain_code(f"В строке '{line}' интерпретатор выполняет операцию по вызову функции '{function.name}'")
                        result = cls.call_function(function, LineList.empty(), context, line_index, code).result
            elif len(v) > 1:
                if variable:
                    def get_values(op: str) -> (str, bool):
                        try:
                            can_set = v[0].endswith(op) or v[1].startswith(op) or v[2].startswith(op)

                            remove_count = len(v[0])
                            if v[0].endswith(op) or v[2].startswith(op):
                                remove_count += 3
                            elif v[1].startswith(op):
                                remove_count += 4
                            new_value = execute_here(line[remove_count:]).result
                            return new_value, can_set
                        except:
                            return 0, True

                    op = Operators.Set.get()
                    if Operators.Set.get() in line:
                        op = Operators.Set.get()
                        info = get_values(op)

                        if Variable.get_type(info[0]) != variable.type:
                            Parser.drop_exception(f"It is not possible to explicitly convert an {Variable.get_type(info[0]).name} type to a {variable.type.name}! At {code.get_line(line_index)}")
                        if info[1]:
                            explain_code(f"В строке '{line}' интерпретатор выполняет математическую операцию '{variable.name} = {info[0]}'")
                            variable.value = info[0]
                        else:
                            Parser.drop_exception(f"Missing '{op}' in variable set! At {code.get_line(line_index)}")
                    elif Operators.AddApply.get() in line:
                        op = Operators.AddApply.get()
                        info = get_values(op)

                        if info[1]:
                            if variable.is_digit:
                                variable.value = str(int(variable.value) + int(info[0]))
                            else:
                                variable.value = variable.value[:-1] + info[0] + "\""
                            explain_code(f"В строке '{line}' интерпретатор выполняет математическую операцию '{variable.name}' + '{info[0]}' и задаёт полученное значение '{variable.name}'")
                        else:
                            Parser.drop_exception(f"Missing '{op}' in variable add! At {code.get_line(line_index)}")
                    elif Operators.DenyApply.get() in line:
                        op = Operators.DenyApply.get()
                        info = get_values(op)

                        if info[1]:
                            if variable.is_digit:
                                variable.value = str(int(variable.value) - int(info[0]))
                                explain_code(f"В строке '{line}' интерпретатор выполняет математическую операцию '{variable.name}' - '{info[0]}' и задаёт полученное значение '{variable.name}'")
                            else:
                                Parser.drop_exception(f"You trying to take away from string! At {code.get_line(line_index)}")
                        else:
                            Parser.drop_exception(f"Missing '{op}' in variable add! At {code.get_line(line_index)}")
                    elif Operators.MultiplyApply.get() in line:
                        op = Operators.MultiplyApply.get()
                        info = get_values(op)

                        if info[1]:
                            if variable.is_digit:
                                variable.value = str(int(variable.value) * int(info[0]))
                                explain_code(f"В строке '{line}' интерпретатор выполняет математическую операцию '{variable.name}' * '{info[0]}' и задаёт полученное значение '{variable.name}'")
                            else:
                                Parser.drop_exception(f"You trying to multiply string! At {code.get_line(line_index)}")
                        else:
                            Parser.drop_exception(f"Missing '{op}' in variable add! At {code.get_line(line_index)}")
                    elif Operators.DivideApply.get() in line:
                        op = Operators.DivideApply.get()
                        info = get_values(op)

                        if info[1]:
                            if variable.is_digit:
                                variable.value = str(int(variable.value) / int(info[0]))
                                explain_code(f"В строке '{line}' интерпретатор выполняет математическую операцию '{variable.name}' / '{info[0]}' и задаёт полученное значение '{variable.name}'")
                            else:
                                Parser.drop_exception(f"You trying to divide string! At {code.get_line(line_index)}")
                        else:
                            Parser.drop_exception(f"Missing '{op}' in variable add! At {code.get_line(line_index)}")
                    elif Operators.SqrtApply.get() in line:
                        op = Operators.SqrtApply.get()
                        info = get_values(op)

                        if info[1]:
                            if variable.is_digit:
                                variable.value = str(math.sqrt(int(variable.value)))
                                explain_code(f"В строке '{line}' интерпретатор выполняет математическую операцию корень из '{variable.name}' и задаёт полученное значение '{variable.name}'")
                            else:
                                Parser.drop_exception(f"You trying to apply sqrt to string! At {code.get_line(line_index)}")
                        else:
                            Parser.drop_exception(f"Missing '{op}' in variable add! At {code.get_line(line_index)}")


                elif function:
                    args = v[1]
                    can_continue = v[1] == Operators.Move.get() or v[2].startswith(Operators.Move.get())
                    if v[1] == Operators.Move.get(): args = v[2]
                    if can_continue:
                        result = cls.call_function(function, get_in(args), context, line_index, code).result
                        explain_code(f"В строке '{line}' интерпретатор выполняет операцию по вызову функции '{function.name}' с аргументами '{function.req_args.line_text}'")
        elif Variable.get_type(line) == VariableType.String:
            result = tool.open_string(line)
        else:
            result = line
            explain_code(f"В строке '{line}' интерпретатор возвращает эту строку без изменений")

        execution_result = ExecutionResult(result, context, Command(command, command_value))
        if CONFIG.debug or (CONFIG.debug and CONFIG.only_return_results): print(f"<execute_line> ({line_index}) context:{context.number} -> line={line} ; result={execution_result} ; \n     full context:\n{context.context}\n\n")
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
    def drop_exception(cls, message: str) -> None:
        print(f"Выполнение кода завершено ошибкой: {Fore.RED + message + Fore.RESET}")
        cls.drop_wait()
        exit()

    @classmethod
    def drop_wait(cls) -> None: input("Press ENTER to continue...")
