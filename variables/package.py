from new_types.package_result import PackageResult
from new_types.type_context import TypeContext


class Package:
    slots = ["__path", "__body"]
    def __init__(self, path: str):
        self.__path = f"{path}.py"
        self.__name = path.split("/")[-1].split(".")[0]
        self.__body = open(self.__path, "r", encoding="utf-8").read()

    @property
    def path(self) -> str: return self.__path

    @property
    def body(self) -> str: return self.__body

    @property
    def name(self) -> str: return self.__name

    def invoke(self, args: list) -> PackageResult:
        cls = args[0]
        line = args[1]
        context = args[2]
        line_index = args[3]
        code = args[4]
        types = args[5]
        namespace = {}
        exec(self.__body, namespace)

        if "get" in namespace:
            result = namespace["get"](cls, line, context, line_index, code, types)
            return result

    def get_new_types(self) -> TypeContext:
        namespace = {}
        exec(self.__body, namespace)

        if "types" in namespace:
            return namespace["types"]()
