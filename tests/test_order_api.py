import pytest
import requests
import allure
from config import BASE_URL

class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цветов (ожидается track в ответе)")
    @pytest.mark.parametrize("color_payload", [
        {},                             
        {"color": ["BLACK"]},           
        {"color": ["GREY"]},            
        {"color": ["BLACK", "GREY"]},   
    ])
    def test_create_order_with_different_colors(self, color_payload):
        """Можно создать заказ с разными вариантами цветов; в ответе есть track."""
        payload = {**color_payload}
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "track" in data


class TestGetOrders:

    @allure.title("Получение списка заказов: возвращается список или объект с полем orders")
    def test_get_orders_returns_list(self):
        """Ручка списка заказов возвращает список."""
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) or (isinstance(data, dict) and "orders" in data)
