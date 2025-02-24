class NeonType:
    slots = ["__name__", "__condition__"]
    def __init__(self, name: str, condition: lambda: None):
        self.__name__ = name
        self.__condition__ = condition

    @property
    def name(self) -> str: return self.__name__

    def confirm(self, value) -> bool: return self.__condition__(value)
