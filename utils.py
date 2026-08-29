import random
import string

def generate_code(length=8):
    """Генерирует случайный код из букв и цифр"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))