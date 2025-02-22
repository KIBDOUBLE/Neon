class PackageResult:
    slots = ["__execution_result", "__result"]
    def __init__(self, execution_result, result: bool):
        self.__execution_result = execution_result
        self.__result = result

    @property
    def execution_result(self): return self.__execution_result

    @property
    def result(self) -> bool: return self.__result
