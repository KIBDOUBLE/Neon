from new_types.command import Command
from variables.variables import Variables


class ExecutionResult:
    slots = ["__result", "__variables", "__reader_command"]
    def __init__(self, result: str, edited_variables: Variables, reader_command: Command):
        self.__result = result
        self.__variables = edited_variables
        self.__reader_command = reader_command

    def contains_result(self) -> bool: return (self.__result != "") and (not self.__result is None)

    @property
    def result(self) -> str: return self.__result

    @property
    def command(self) -> Command: return self.__reader_command

    @property
    def variables(self) -> Variables: return self.__variables

    @staticmethod
    def is_execution_result(string: str) -> bool: return str(string).startswith("(result:") and ", CN" in str(string)

    @classmethod
    def restore(cls, string: str):
        result = ""
        command = 0
        command_value = 0

        from tool import get_in
        data = get_in(string)
        for cell in data.lines:
            cell: str
            if cell.startswith("result:"): result = cell[7:]
            elif cell.startswith("command:"):
                data1 = cell[8:].split(":")
                command = int(data1[0])
                command_value = int(data1[1])

        return ExecutionResult(result, Variables(2), Command(command, command_value))


    def __str__(self) -> str: return f"(result:{self.__result}, CN:{self.__variables.number}, command:{self.__reader_command})"
