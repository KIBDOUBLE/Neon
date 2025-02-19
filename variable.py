class Variable:
    slots = ["__name", "value"]
    def __init__(self, name: str, value: str):
        self.__name = name
        self.value = value

    @property
    def name(self) -> str: return self.__name
