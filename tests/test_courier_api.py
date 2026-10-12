import pytest
import allure
from helpers.courier_helper import create_courier, login_courier  


class TestCreateCourier:
    @allure.title("Успешная регистрация курьера (ожидается 201 Created)")
    def test_create_courier_success(self, registered_courier):
        """Курьер успешно создаётся, возвращается ok: true и код 201."""
        data = registered_courier["data"]
        assert "id" in data, "В ответе нет поля 'id'"
        assert data.get("ok") is True, "Поле 'ok' не равно True"

    @allure.title("Ошибка при создании курьера без обязательного поля (login или password)")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field, registered_courier):
        """Если не передать обязательное поле, API возвращает ошибку (не 201)."""
        payload = {
            "login": registered_courier["payload"]["login"],
            "password": registered_courier["payload"]["password"],
            "firstName": registered_courier["payload"]["first_name"],
        }

        del payload[missing_field]
        response = create_courier(payload)

        assert response.status_code != 201, f"Ожидалась ошибка при отсутствии {missing_field}, но получен статус {response.status_code}"
        
        data = response.json()
        assert not data.get("ok", True), "В ответе не указано, что операция не удалась"

    @allure.title("Нельзя создать курьера с дублирующимся логином (ожидается 409)")
    def test_create_duplicate_courier(self, registered_courier):
        payload = registered_courier["payload"].copy()
        second_response = create_courier(payload)
        
        assert second_response.status_code == 409, f"Не получен статус 409 при дублировании логина, получен: {second_response.status_code}"
        data = second_response.json()
        assert not data.get("ok", True), "При дубликате логина поле 'ok' должно быть False"


class TestCourierLogin:
    @allure.title("Успешный логин курьера (используем фикстуру для создания)")
    def test_login_success(self, registered_courier):
        """Логин курьера: создаём через фикстуру, затем логинимся, ожидаем 200 и наличие id в ответе."""
        login = registered_courier["payload"]["login"]
        password = registered_courier["payload"]["password"]

        login_payload = {
            "login": login,
            "password": password,
        }
 
        resp_login = login_courier(login_payload)
        
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
        response = login_courier(payload)
        assert response.status_code != 200, "Ожидалась ошибка аутентификации, но получен успешный статус"
        data = response.json()
        assert not data.get("ok", True), "При неверных данных поле 'ok' должно быть False"

    @allure.title("Ошибка, если не передать обязательное поле для логина")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field, registered_courier):
        login = registered_courier["payload"]["login"]
        password = registered_courier["payload"]["password"]

        payload = {"login": login, "password": password}
        del payload[missing_field]

        response = login_courier(payload)
        assert response.status_code != 200, f"Ожидалась ошибка из‑за отсутствия {missing_field}, но получен статус {response.status_code}"
        data = response.json()
        assert not data.get("ok", True), "При отсутствии обязательного поля поле 'ok' должно быть False"
