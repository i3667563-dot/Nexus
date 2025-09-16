import string
import random

def generate(num: int, ABC: bool, abc: bool, spech_simbols: bool) -> str:
    chars = ''
    if ABC == True:
        chars += string.ascii_uppercase
    if abc == True:
        chars += string.ascii_lowercase
    if spech_simbols == True:
        chars += string.punctuation

    if not chars:
        print('Не выбраны условия')

    password = ''.join(random.choice(chars) for _ in range(num))
    print(f"🔐 Сгенерирован пароль: {password}")


def proverka(password: str) -> int:
    """
    Оценивает надёжность пароля по шкале от 0 до 10.
    
    Критерии:
    - 1 балл: длина ≥ 8 символов
    - 1 балл: длина ≥ 12 символов
    - 1 балл: длина ≥ 16 символов
    - 1 балл: содержит хотя бы одну цифру
    - 1 балл: содержит хотя бы одну заглавную букву
    - 1 балл: содержит хотя бы одну строчную букву
    - 1 балл: содержит хотя бы один спецсимвол из списка
    - 1 балл: содержит 3+ спецсимвола
    - 1 балл: не содержит повторяющихся символов подряд (например, "aaa")
    - 1 балл: не содержит простых слов (password, 123456, qwerty и т.д.)

    Возвращает: int от 0 до 10
    """

    if not isinstance(password, str):
        return 0

    score = 0
    password = password.strip()

    COMMON_PASSWORDS = {
        'password', '123456', '123456789', 'qwerty', 'abc123',
        'password123', 'admin', 'letmein', 'welcome', 'monkey',
        '1234567', '12345678', '12345', 'iloveyou', 'princess',
        '1234567890', '123123', 'dragon', 'baseball', 'football'
    }

    SPECIAL_CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?/`~'

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if len(password) >= 16:
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c in SPECIAL_CHARS for c in password):
        score += 1

    if sum(1 for c in password if c in SPECIAL_CHARS) >= 3:
        score += 1

    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:

            score = max(0, score - 1)
            break

    if password.lower() not in COMMON_PASSWORDS:
        score += 1

    print(min(max(score, 0), 10))