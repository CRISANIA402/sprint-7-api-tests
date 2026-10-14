
import requests
from config import BASE_URL

def create_courier(payload: dict):
    """Отправляет POST-запрос на создание курьера."""
    return requests.post(f"{BASE_URL}/courier", json=payload)

def login_courier(payload: dict):
    """Отправляет POST-запрос на логин курьера."""
    return requests.post(f"{BASE_URL}/courier/login", json=payload)

def delete_courier(courier_id: int):
    """Отправляет DELETE-запрос на удаление курьера по ID."""
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")