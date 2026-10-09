import pytest
import random
import string
from config import BASE_URL

def generate_unique_login():
    prefix = "uniq_"
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return prefix + random_part

@pytest.fixture
def new_courier():
    """Возвращает только данные для курьера: логин, пароль, first_name.
     Не делает запросы к API — это задача тестов."""
    login = generate_unique_login()
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    first_name = ''.join(random.choices(string.ascii_lowercase, k=8))

    return {
        "login": login,
        "password": password,
        "first_name": first_name,
    }
