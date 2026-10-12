import requests
from config import BASE_URL

def create_order(payload: dict):
    return requests.post(f"{BASE_URL}/orders", json=payload)


def get_orders():
    return requests.get(f"{BASE_URL}/orders")
