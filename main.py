import os.path

from parser import Parser

if __name__ == "__main__":
    file_path = f"{input("File: ")}.neon"
    if not os.path.exists(file_path):
        while not os.path.exists(f"{file_path}"):
            file_path = f"{input("Retry:\nFile: ")}.neon"
    p = Parser(open(file_path, 'r').read())
    p.execute()
