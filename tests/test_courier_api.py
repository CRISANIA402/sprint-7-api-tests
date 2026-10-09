import time
import random
import string
import pytest
import requests
import allure
from helpers.courier_helper import generate_random_string
from config import BASE_URL


class TestCreateCourier:
    @allure.title("Успешная регистрация курьера (201 Created)")
    def test_create_courier_success(self, new_courier):
        """Курьер успешно создаётся, возвращается ok: true и код 201."""
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": new_courier["first_name"],
        }
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 201
        data = response.json()
        assert data.get("ok") is True

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field, new_courier):
        """Если не передать обязательное поле, API возвращает ошибку."""
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": new_courier["first_name"],
        }

        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier", data=payload)

        assert response.status_code != 201

    @allure.title("Нельзя создать курьера с дублирующимся логином")
    def test_create_duplicate_courier(self):
        """Создаём курьера, потом пытаемся создать ещё раз с тем же логином — получаем 409."""
        login = "dup_test_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        password = "pass_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        first_name = "name_" + "".join(random.choices(string.ascii_lowercase, k=6))

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }

        @allure.step("Сначала регистрируем курьера (ожидаем 201)")
        def register_first():
            return requests.post(f"{BASE_URL}/courier", data=payload)

        first_response = register_first()
        assert first_response.status_code in (201, 409)

        @allure.step("Пробуем зарегистрировать второго курьера с тем же логином (ожидаем 409)")
        def try_duplicate():
            return requests.post(f"{BASE_URL}/courier", data=payload)

        second_response = try_duplicate()
        assert second_response.status_code == 409


class TestCourierLogin:
    @allure.title("Успешный логин курьера (автономный тест: создание + логин)")
    def test_login_success(self):
        """Создаём курьера и сразу логинимся, чтобы исключить проблемы с фикстурами."""
        
        login = "test_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        password = "pass_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        first_name = "Name_" + "".join(random.choices(string.ascii_lowercase, k=6))

        create_payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }

        resp_create = requests.post(f"{BASE_URL}/courier", data=create_payload)
        assert resp_create.status_code in (201, 409), f"Не удалось создать курьера: {resp_create.status_code}, {resp_create.text}"

        if resp_create.status_code == 409:
            login = "test_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
            create_payload["login"] = login
            resp_create = requests.post(f"{BASE_URL}/courier", data=create_payload)
            assert resp_create.status_code == 201, f"Повторное создание курьера не удалось: {resp_create.status_code}"

        time.sleep(3)

        login_payload = {
            "login": login,
            "password": password,
        }
        resp_login = requests.post(f"{BASE_URL}/courier/login", data=login_payload)

        assert resp_login.status_code == 200, f"Логин не прошёл: {resp_login.status_code}, ответ: {resp_login.text}"
        data = resp_login.json()
        assert "id" in data, f"В ответе нет поля 'id'. Полный ответ: {data}"

    @allure.title("Ошибка при неверном логине или пароле")
    @pytest.mark.parametrize("wrong_field", [
        {"login": "wrong_login", "password": "any_password"},
        {"login": "any_login", "password": "wrong_password"},
    ])
    def test_login_wrong_credentials(self, wrong_field):
        payload = wrong_field
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code != 200

    @allure.title("Ошибка, если не передать обязательное поле для логина")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field):
        login = "temp_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        password = "temp_pass_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        create_payload = {"login": login, "password": password, "firstName": "Temp"}
        resp = requests.post(f"{BASE_URL}/courier", data=create_payload)
        if resp.status_code not in (201, 409):
            pytest.fail(f"Не удалось подготовить курьера для теста: {resp.status_code}")

        time.sleep(2)

        payload = {"login": login, "password": password}
        del payload[missing_field]
        
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code != 200
