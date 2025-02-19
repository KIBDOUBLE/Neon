class LineList:
    slots = ["lines"]
    def __init__(self, lines: list):
        self.__lines: list = lines

    def get_line(self, index) -> str: return self.__lines[index]

    def length(self) -> int: return len(self.__lines)

    @classmethod
    def empty(cls): return LineList([])

    @property
    def lines(self) -> list: return self.__lines.copy()

    @property
    def text(self) -> str: return "\n".join(self.__lines)


def create(lines: str) -> LineList: return LineList(lines.split('\n'))
