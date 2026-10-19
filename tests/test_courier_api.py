import pytest
import allure
import uuid
from helpers.courier_helper import create_courier, login_courier


class TestCreateCourier:
    @allure.title("Успешная регистрация курьера")
    def test_create_courier_success(self):
        unique_login = f"courier_{uuid.uuid4().hex[:8]}"
        payload = {
            "login": unique_login,
            "password": "secret123",
            "firstName": "TestName",
        }

        response = create_courier(payload)

        assert response.status_code == 201, (
            f"Ожидается статус 201, получен {response.status_code}. Ответ: {response.text}"
        )

        data = response.json()
        assert data.get("ok") is True, f"Ожидается ok: True, получен: {data}"

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

        data = second_response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"
        assert data["code"] == 409


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

        data = resp_login.json()
        assert "id" in data, f"В ответе нет поля 'id'. Полный ответ: {data}"

    @allure.title("Ошибка аутентификации при неверных данных (ожидается 404)")
    @pytest.mark.parametrize("payload,expected_status", [
        ({"login": "wrong", "password": "correct"}, 404),
        ({"login": "correct", "password": "wrong"}, 404),
    ])
    def test_login_wrong_credentials(self, payload, expected_status):
        response = login_courier(payload)
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}"
        )

        data = response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"
        assert data["code"] == expected_status

    @allure.title("Ошибка, если не передать обязательное поле для логина (ожидается 400)")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }
        del payload[missing_field]

        response = login_courier(payload)
        expected_status = 400

        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status} при отсутствии {missing_field}, "
            f"получен {response.status_code}"
        )

        data = response.json()
        assert "code" in data, "В ответе нет поля code"
        assert "message" in data, "В ответе нет поля message"
        assert data["code"] == expected_status
