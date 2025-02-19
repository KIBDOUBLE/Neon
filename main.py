from parser import Parser

if __name__ == "__main__":
    p = Parser(open("test.neon", 'r').read())
    p.execute()
