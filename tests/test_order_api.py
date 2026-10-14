import pytest
import allure
from helpers.order_helper import create_order, get_orders

class TestCreateOrder:
    @allure.title("Создание заказа с разными вариантами цветов (ожидается track в ответе)")
    @pytest.mark.parametrize("color_list", [
        [],                             
        ["BLACK"],                     
        ["GREY"],                       
        ["BLACK", "GREY"],             
    ])
    def test_create_order_with_different_colors(self, color_list):
        """Можно создать заказ с разными вариантами цветов; в ответе есть track."""
        payload = {"color": color_list}

        response = create_order(payload)
        assert response.status_code == 201, f"Не удалось создать заказ: {response.status_code}, {response.text}"

        data = response.json()
        assert "track" in data, "В ответе нет поля track"

        assert isinstance(data["track"], str), "Поле track должно быть строкой"


class TestGetOrders:
    @allure.title("Получение списка заказов: возвращается список или объект с полем orders")
    def test_get_orders_returns_list(self):
        """Ручка списка заказов возвращает список либо объект с полем orders."""
        response = get_orders()
        assert response.status_code == 200, f"Запрос списка заказов не удался: {response.status_code}, {response.text}"

        data = response.json()

        assert (
            isinstance(data, list)
            or (isinstance(data, dict) and "orders" in data)
        ), "Ответ не соответствует ожидаемой структуре (список либо dict с ключом orders)"

