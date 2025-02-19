from variables import Variables


class ExecutionResult:
    slots = ["__result", "__variables"]
    def __init__(self, result: str, edited_variables: Variables):
        self.__result = result
        self.__variables = edited_variables

    def contains_result(self) -> bool: return (self.__result != "") and (not self.__result is None)

    @property
    def result(self) -> str: return self.__result

    @property
    def variables(self) -> Variables: return self.__variables
