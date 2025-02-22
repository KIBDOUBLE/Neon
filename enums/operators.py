from enum import Enum

from PyInstaller.isolated import Python


class Operators(Enum):
    Python = "~",
    Expression = "@",
    Ignore = "#",
    End = "***"
    Set = "<-",
    Move = "->",
    AddApply = "+=",
    DenyApply = "-=",
    MultiplyApply = "*=",
    DivideApply = "/=",
    SqrtApply = "<sqrt",
    Add = "+",
    Deny = "-",
    Multiply = "*",
    Divide = "/",
    Exponentiation = "**"

    @classmethod
    def all(cls): return (f"{cls.Python.get()}{cls.Expression.get()}{cls.Ignore.get()}"
                          f"{cls.End.get()}{cls.Set.get()}{cls.Move.get()}"
                          f"{cls.AddApply.get()}{cls.DenyApply.get()}{cls.MultiplyApply.get()}"
                          f"{cls.DivideApply.get()}{cls.SqrtApply.get()}{cls.Add.get()}"
                          f"{cls.Deny.get()}{cls.Multiply.get()}{cls.Divide.get()}"
                          f"{cls.Exponentiation.get()}")

    def get(self): return self.value[0]
