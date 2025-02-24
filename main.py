import os.path

from neon_parser import NeonParser

if __name__ == "__main__":
    file_path = f"{input("File: ")}.neon"
    if not os.path.exists(file_path):
        while not os.path.exists(f"{file_path}"):
            file_path = f"{input("Retry:\nFile: ")}.neon"
    p = NeonParser(open(file_path, 'r').read())
    p.execute()
