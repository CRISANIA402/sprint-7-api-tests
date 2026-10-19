import requests
import allure
from config import BASE_URL


@allure.step("POST /courier — создание курьера")
def create_courier(payload: dict):
    """Отправляет POST-запрос на создание курьера."""
    return requests.post(f"{BASE_URL}/courier", json=payload, timeout=60)


@allure.step("POST /courier/login — логин курьера")
def login_courier(payload: dict):
    """Отправляет POST-запрос на логин курьера."""
    return requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=60)
