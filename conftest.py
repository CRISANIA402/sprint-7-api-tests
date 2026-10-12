import pytest
import random
import string
from helpers.courier_helper import create_courier 

def generate_unique_login():
    prefix = "uniq_"
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return prefix + random_part

@pytest.fixture
def registered_courier():
    login = generate_unique_login()
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    first_name = ''.join(random.choices(string.ascii_lowercase, k=8))

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    response = create_courier(payload)
    
    if response.status_code == 409:
        pytest.fail(f"Логин {login} уже занят в базе. Это редкий случай на общем стенде.")

    assert response.status_code == 201, f"Не удалось создать курьера: {response.status_code}, {response.text}"

    data = response.json()
    assert "id" in data, "В ответе нет поля id"
    assert data["login"] == login, "Логин в ответе не совпадает с отправленным"
    assert data.get("firstName") == first_name, "firstName в ответе не совпадает"

    yield {
        "payload": payload,
        "response": response,
        "data": data,
    }

