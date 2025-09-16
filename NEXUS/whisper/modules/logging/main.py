# whisper/modules/logging/main.py

import os
from pathlib import Path

class Whisper:
    def log(self, message: str):
        """
        Записывает сообщение в .nexus/whisper.log.
        Не меняет cwd. Не зависит от внешнего контекста.
        Работает даже если .nexus ещё не существует.
        """
        try:
            # Получаем путь к APPDATA
            appdata = os.getenv('APPDATA')
            if not appdata:
                return False  # Не смогли найти APPDATA — просто молчим

            # Путь к файлу лога
            nexus_path = Path(appdata) / ".nexus"
            log_file = nexus_path / "whisper.log"

            # Создаём папку, если её нет
            nexus_path.mkdir(parents=True, exist_ok=True)

            # Получаем текущее время в формате ISO (2025-04-06T12:34:22)
            from datetime import datetime
            timestamp = datetime.now().isoformat(timespec='seconds')

            # Записываем строку
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")

            return True  # Успешно записано

        except Exception:
            # Любая ошибка — игнорируем. Это тихий журнал.
            # Ты не хочешь, чтобы он ломал систему.
            return False