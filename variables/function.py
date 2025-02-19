from types.line_list import LineList


class Function:
    slots = ["__name", "body", "req_args"]
    def __init__(self, name: str, body: LineList, req_args: LineList):
        self.__name = name
        self.body = body
        self.req_args = req_args

    @property
    def name(self) -> str: return self.__name
