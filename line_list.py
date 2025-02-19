class LineList:
    slots = ["lines"]
    def __init__(self, lines: list):
        self.__lines: list = lines

    def get_line(self, index) -> str: return self.__lines[index]

    def length(self) -> int: return len(self.__lines)

    @property
    def lines(self) -> list: return self.__lines.copy()


def create(lines: str) -> LineList: return LineList(lines.split('\n'))
