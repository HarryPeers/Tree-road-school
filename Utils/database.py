from os import path, getcwd
from json import load, dump, decoder

class database:
    def __init__(self):
        self.cwd = getcwd()
        self.path = f"{self.cwd}/database.json"
        
        self.data = None
        self.password = None

        self.load_password()
        self.load()

    def load_password(self):
        with open(f"{self.cwd}/password.txt") as file:
            self.password = file.read().splitlines()[0].strip()

    def load(self):
        if not self.exists:
            self.create()
        else:
            try:
                with open(self.path) as file:
                    self.data = load(file)
            except decoder.JSONDecodeError:
                self.create()

    def create(self):
        self.data = {}
        self.write()

    def write(self):
        with open(self.path, "w") as file:
            dump(self.data, file, indent=3)

    @property
    def exists(self):
        return path.exists(self.path)
        
        
