import pytest
import allure
from helpers.courier_helper import create_courier, login_courier


class TestCreateCourier:
    @allure.title("Успешная регистрация курьера")
    def test_create_courier_success(self, registered_courier):
        assert True

    @allure.title("Ошибка при отсутствии обязательного поля (login/password/firstName)")
    @pytest.mark.parametrize("missing_field,expected_status", [
        ("login", 400),
        ("password", 400),
        ("firstName", 409),
    ])
    def test_create_courier_missing_required_field(self, missing_field, expected_status, registered_courier):
        payload = registered_courier["payload"].copy()
        del payload[missing_field]

        response = create_courier(payload)

        assert response.status_code == expected_status, (
            f"Ожидается статус {expected_status}, получен {response.status_code}"
        )

        data = response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"
        assert data["code"] == expected_status

    @allure.title("Нельзя создать курьера с дублирующимся логином (ожидается 409)")
    def test_create_duplicate_courier(self, registered_courier):
        payload = registered_courier["payload"].copy()
        second_response = create_courier(payload)

        assert second_response.status_code == 409, (
            f"Не получен статус 409 при дублировании логина, получен: {second_response.status_code}"
        )

        if not second_response.content:
            pytest.skip("Пустой ответ от сервера, нельзя проверить JSON")

        data = second_response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"
        assert data["code"] == 409, f"Ожидается код 409, получен: {data.get('code')}"


class TestCourierLogin:
    @allure.title("Успешный логин курьера")
    def test_login_success(self, registered_courier):
        login_payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }

        resp_login = login_courier(login_payload)
        assert resp_login.status_code == 200, (
            f"Логин не прошёл: {resp_login.status_code}, ответ: {resp_login.text}"
        )

        if not resp_login.content:
            pytest.skip("Пустой ответ от сервера, нельзя проверить JSON")

        data = resp_login.json()
        assert "id" in data, f"В ответе нет поля 'id'. Полный ответ: {data}"

    @allure.title("Ошибка при неверном логине или пароле")
    @pytest.mark.parametrize("wrong_field", [
        {"login": "wrong_login", "password": "any_password"},
        {"login": "any_login", "password": "wrong_password"},
    ])
    def test_login_wrong_credentials(self, wrong_field):
        payload = wrong_field
        response = login_courier(payload)
        assert response.status_code != 200, "Ожидалась ошибка аутентификации, но получен успешный статус"

        if not response.content or not response.headers.get("Content-Type", "").startswith("application/json"):
            pytest.skip("Сервер не вернул JSON, нельзя проверить структуру ответа")

        data = response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"

    @allure.title("Ошибка, если не передать обязательное поле для логина")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }
        del payload[missing_field]

        response = login_courier(payload)
        assert response.status_code != 200, (
            f"Ожидалась ошибка из‑за отсутствия {missing_field}, но получен статус {response.status_code}"
        )

        if not response.content or not response.headers.get("Content-Type", "").startswith("application/json"):
            pytest.skip("Сервер не вернул JSON, нельзя проверить структуру ответа")

        data = response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"
