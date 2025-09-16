import pit.modules.file.main as main

class File():
    def __init__(self):
        self.delete = main.delete
        self.create = main.create
        self.rename = main.rename