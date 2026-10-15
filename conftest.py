import pytest
import random
import string
from helpers.courier_helper import create_courier

@pytest.fixture
def registered_courier():
    login = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    first_name = ''.join(random.choices(string.ascii_lowercase, k=8))

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    response = create_courier(payload)
    assert response.status_code == 201, f"Курьер не создан. Статус: {response.status_code}, ответ: {response.text}"

    data = response.json() if response.content else {}
    yield {
        "login": login,
        "password": password,
        "first_name": first_name,
        "payload": payload,
        "response": data,
    }
