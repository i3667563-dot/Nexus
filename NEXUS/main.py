import os

import build

app = build.Nexus()

def create_nexus_folder():
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("Не удалось получить путь к AppData\\Roaming")
        return

    nexus_path = os.path.join(appdata, '.nexus')

    if not os.path.exists(nexus_path):
        os.mkdir(nexus_path)
        print(f'Папка создана: {nexus_path}')
    else:
        pass

create_nexus_folder()

app.start()

'''for i in range(10000):
    app.create_file(f'{i+1}', 'txt')
for i in range(10000):
    app.rename_file(f'{i+1}.txt', f'test_{i+1}')
for i in range(10000):
    app.delete_file(f'test_{i+1}')'''