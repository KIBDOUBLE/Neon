from new_types.neon_type import NeonType


class TypeContext:
    slots = ["__data__"]
    def __init__(self):
        self.__data__ = {}

    @property
    def data(self) -> dict: return self.__data__.copy()

    def get(self, type_name: str) -> NeonType: return self.__data__[type_name]

    def register(self, type: NeonType) -> None: self.__data__[type.name] = type

    def join(self, context) -> None:
        if not context: return
        for key in context.data:
            if not key in self.__data__:
                self.__data__[key] = context.data[key]
