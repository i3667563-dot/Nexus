# vault/main.py — обновлённая версия

import os
import base64
import uuid
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Vault:
    def __init__(self):
        self.path = Path(os.getenv('APPDATA', '')) / '.nexus' / 'vault.db'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        if not self.path.exists():
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return eval(f.read())
        except:
            return {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(str(self.data))

    def create_note(self, password: str, content: str) -> str:
        note_id = str(uuid.uuid4())
        key = self._derive_key_from_password(password)
        f = Fernet(key)
        encrypted = f.encrypt(content.encode())
        self.data[note_id] = base64.b64encode(encrypted).decode()
        self._save()
        return note_id

    def open_note(self, note_id: str, password: str) -> str | None:
        if note_id not in self.data:
            return None
        try:
            key = self._derive_key_from_password(password)
            f = Fernet(key)
            decrypted = f.decrypt(base64.b64decode(self.data[note_id]))
            return decrypted.decode()
        except Exception:
            return None

    def list_notes(self) -> list[str]:
        return list(self.data.keys())

    # ✅ ИСПРАВЛЕНИЕ: delete_note теперь требует пароль!
    def delete_note(self, note_id: str, password: str) -> bool:
        """
        Удаляет заметку ТОЛЬКО если пароль совпадает.
        Никто не может удалить — даже зная ID — без пароля.
        """
        if note_id not in self.data:
            return False

        # Проверяем, можно ли открыть — это и есть проверка пароля
        if self.open_note(note_id, password) is None:
            return False  # Неверный пароль — нельзя удалять!

        # Только если пароль верный — удаляем
        del self.data[note_id]
        self._save()
        return True

    def _derive_key_from_password(self, password: str) -> bytes:
        salt = (password + "NEXUS_VAULT_SALT").encode()[:16].ljust(16, b'\x00')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))