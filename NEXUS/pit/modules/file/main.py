import os

def rename(path:str, new_name:str):
    os.rename(path, new_name)

def create(file_name:str, end:str):
    with open(f'{file_name}.{end}', 'wb') as file:
        pass

def delete(path:str):
    os.remove(path)