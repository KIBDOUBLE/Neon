from new_types.package_result import PackageResult


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
        line = args[0]
        context = args[1]
        line_index = args[2]
        code = args[3]
        namespace = {}
        exec(self.__body, namespace)

        if "get" in namespace:
            result = namespace["get"](line, context, line_index, code)
            return result
