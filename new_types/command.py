import parser


class Command:
    slots = ["__command__", "__value__"]
    def __init__(self, command: int, value=None):
        self.__command__ = command
        self.__value__ = value

    def set_value(self, new_value, accessor):
        if accessor is parser.Parser:
            self.__value__ = new_value
        else:
            parser.Parser.drop_exception("You trying to change value of command without required allowed accessor!")

    def set_command(self, new_command: int, accessor):
        if accessor is parser.Parser:
            self.__command__ = new_command
        else:
            parser.Parser.drop_exception("You trying to change command without required allowed accessor!")

    @property
    def command(self) -> int: return self.__command__

    @property
    def s_value(self) -> str: return str(self.__value__)

    @property
    def i_value(self) -> int: return int(self.__value__)

    def __str__(self) -> str: return f"Reader Command -> {self.__command__}:{self.__value__}"