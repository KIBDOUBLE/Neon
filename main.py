from parser import Parser
from tool import tab_clear

if __name__ == "__main__":
    p = Parser(open("test.neon", 'r').read())
    p.execute()
