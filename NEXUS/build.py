import os
from pathlib import Path

import pit.modules.file.api as pitF
import passy.modules.password.api as passyPass
import eras.modules.clear.api as erasC
import whisper.modules.logging.api as whisperLog
import vault.modules.secrets.api as vaultAPI

# -------------------------------
# 🌿 Инициализация внешних модулей
# -------------------------------
pit_file = pitF.File()
passy_password = passyPass.Password()
eras_clear = erasC.Clear()
whisper_logging = whisperLog.Whisper()
vault = vaultAPI.vault

# -------------------------------
# 🧩 ОРГАНЫ NEXUS — без лишних обёрток
# -------------------------------

class Pit:
    def __init__(self):
        self.delete = pit_file.delete
        self.rename = pit_file.rename
        self.create = pit_file.create


class Passy:
    def __init__(self):
        self.generate = passy_password.generate
        self.check_password = passy_password.check_password
        self.ocenka = passy_password.check_password  # 👈 Исправлено: ocenka, а не check_password


class Eras:
    def __init__(self):
        self.clear_terminal = eras_clear.clear


class Whisper:
    def __init__(self):
        self.log = whisper_logging.log


# -------------------------------
# 🌟 NEXUS — главный организм
# -------------------------------

class Nexus:
    def __init__(self):
        self.passy = Passy()
        self.pit = Pit()
        self.eras = Eras()
        self.whisper = Whisper()

        self.generate_password = self.passy.generate
        self.check_password = self.passy.check_password
        self.create_file = self.pit.create
        self.delete_file = self.pit.delete
        self.rename_file = self.pit.rename
        self.clear_terminal = self.eras.clear_terminal
        self.whisper_log = self.whisper.log

        self.create_note = vault.create_note
        self.open_note = vault.open_note
        self.list_notes = vault.list_notes
        self.delete_note = vault.delete_note

    def start(self):
        print("🪄 NEXUS — готов. Говорите команды. (Введи 'nexus.app exit' для выхода)")
        print("💡 Пример: pit create file diary txt")
        print()

        while True:
            try:
                cmd = input("NEXUS> ").strip()
                if not cmd:
                    continue

                parts = cmd.lower().split()
                if not parts:
                    continue

                # -------------------------------
                # 🛑 Выход
                # -------------------------------
                if parts[0] == "nexus.app" and len(parts) >= 2 and parts[1] in ("exit", "stop"):
                    print("🌙 NEXUS выключен. Всего доброго.")
                    break

                # -------------------------------
                # 📁 PIT
                # -------------------------------
                elif parts[0] == "pit":
                    if len(parts) < 3:
                        print("❌ Неверная команда. Используй: pit <action> file <args>")
                        continue
                    action = parts[1]
                    if parts[2] != "file":
                        print("❌ Ожидалось 'file' после 'pit <action>'.")
                        continue
                    if action == "create" and len(parts) == 5:
                        name, ext = parts[3], parts[4]
                        self.create_file(name, ext)
                        print(f"📄 Создан файл: {name}.{ext}")
                    elif action == "delete" and len(parts) == 4:
                        path = parts[3]
                        self.delete_file(path)
                        print(f"🗑️  Удалён файл: {path}")
                    elif action == "rename" and len(parts) == 5:
                        old, new = parts[3], parts[4]
                        self.rename_file(old, new)
                        print(f"🔄 Переименован: {old} → {new}")
                    else:
                        print("❌ Неизвестная операция.")

                # -------------------------------
                # 🔐 PASSY
                # -------------------------------
                elif parts[0] == "passy":
                    if len(parts) < 2:
                        print("❌ Неверная команда. Используй: passy <action> ...")
                        continue
                    action = parts[1]
                    if action == "generate" and parts[2] == "password" and len(parts) >= 7:
                        length = int(parts[3])
                        use_lower = parts[4].lower() in ("true", "1", "yes")
                        use_upper = parts[5].lower() in ("true", "1", "yes")
                        use_special = parts[6].lower() in ("true", "1", "yes")
                        pwd = self.generate_password(length, use_lower, use_upper, use_special)
                        print(f"🔐 Сгенерирован пароль: {pwd}")
                    elif action == "check" and parts[2] == "password" and len(parts) == 4:
                        pwd = parts[3]
                        score = self.check_password(pwd)
                        print(f"🔒 Оценка: {score}/10 — {self.passy.ocenka(score)}")
                    else:
                        print("❌ Используй: passy generate password <len> <a> <A> <s> или passy check password <pwd>")

                # -------------------------------
                # 🧹 ERAS
                # -------------------------------
                elif parts[0] == "eras":
                    if len(parts) >= 3 and parts[1] == "clear" and parts[2] == "terminal":
                        self.clear_terminal()
                        print("🧹 Терминал очищен.")

                # -------------------------------
                # 💬 WHISPER
                # -------------------------------
                elif parts[0] == "whisper":
                    message = " ".join(parts[1:])
                    if not message:
                        print("💡 Используй: whisper <текст>")
                        continue
                    success = self.whisper_log(message)
                    if success:
                        print("📝 Записано в .nexus/whisper.log")
                    else:
                        print("⚠️  Не удалось записать (права? путь?)")

                # -------------------------------
                # 🔒 VAULT — ЗАМЕТКИ ПО ПАРОЛЮ
                # -------------------------------
                elif parts[0] == "vault":
                    if len(parts) < 2:
                        print("💡 Используй: vault create/open/list/delete <аргументы>")
                        continue

                    action = parts[1]

                    if action == "create" and len(parts) >= 4:
                        password = parts[2]
                        note_content = " ".join(parts[3:])
                        note_id = self.create_note(password, note_content)
                        print(f"🔒 Заметка создана. ID: {note_id}")
                        print("💾 Сохрани этот ID — он нужен для открытия.")

                    elif action == "open" and len(parts) == 4:
                        note_id = parts[2]
                        password = parts[3]
                        content = self.open_note(note_id, password)
                        if content is not None:
                            print(f"🔓 Содержимое заметки #{note_id}:")
                            print(content)
                        else:
                            print("❌ Неверный пароль или ID не найден.")

                    elif action == "list":
                        ids = self.list_notes()
                        if ids:
                            print("🔑 Сохранённые заметки (ID):")
                            for note_id in ids:
                                print(f"  • {note_id}")
                        else:
                            print("📭 Нет сохранённых заметок.")

                    elif action == "delete" and len(parts) == 4:
                        note_id = parts[2]
                        password = parts[3]
                        if self.delete_note(note_id, password):
                            print(f"🗑️  Заметка {note_id} удалена.")
                        else:
                            print("❌ Неверный пароль или заметка не найдена.")

                    else:
                        print("❌ Используй: vault create <пароль> <текст> | open <id> <пароль> | list | delete <id> <пароль>")

                # -------------------------------
                # 🤝 СВЯЗЬ: AUTO-TAGGING С ПАРОЛЕМ ЧЕРЕЗ VAULT
                # -------------------------------
                elif parts[0] == "passy" and parts[1] == "save" and parts[2] == "password":
                    if len(parts) != 4:
                        print("💡 Используй: passy save password <name>")
                        continue
                    name = parts[3]
                    pwd = self.generate_password(24, True, True, True)
                    vault.create_note(name, pwd)  # 👈 ПРЯМО ИСПОЛЬЗУЕМ ВАУЛТ — без прокси!
                    print(f"🔐 Пароль сгенерирован и сохранён в vault под именем '{name}': {pwd}")

                # -------------------------------
                # 🤝 СВЯЗЬ: ВОССТАНОВЛЕНИЕ ПАРОЛЯ ИЗ VAULT В ПИТ
                # -------------------------------
                elif parts[0] == "pit" and parts[1] == "create" and parts[2] == "secret" and len(parts) == 4:
                    name = parts[3]
                    content = vault.open_note(name, name)  # 👈 Открываем по имени как паролю
                    if content is not None:
                        filename = f"{name}.txt"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"📄 Создан файл {filename} с содержимым из vault/{name}")
                    else:
                        print(f"❓ Пароль '{name}' не найден в vault.")

                # -------------------------------
                # ❌ Неизвестная команда
                # -------------------------------
                else:
                    print("❓ Неизвестная команда. Доступные: pit, passy, eras, whisper, vault, nexus.app")

            except KeyboardInterrupt:
                print("\n🌙 NEXUS выключен. Всего доброго.")
                break
            except Exception as e:
                print(f"⚠️  Ошибка: {e}")