from command import Command
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

    def __str__(self) -> str: return f"(result:{self.__result}, CN:{self.__variables.number}, command:{self.__reader_command})"
