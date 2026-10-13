
import requests
from config import BASE_URL

def create_courier(payload: dict):
    """Отправляет POST-запрос на создание курьера."""
    return requests.post(f"{BASE_URL}/courier", json=payload)

def login_courier(payload: dict):
    """Отправляет POST-запрос на логин курьера."""
    return requests.post(f"{BASE_URL}/courier/login", json=payload)

