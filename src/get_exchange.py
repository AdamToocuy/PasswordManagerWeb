import requests

# Базовый URL
API_URL = "https://open.er-api.com/v6/latest/"

def get_currency_data(base="USD"):
    """Получает полные данные (все курсы) относительно базовой валюты."""
    try:
        response = requests.get(f"{API_URL}{base}", timeout=5)
        if response.status_code == 200:
            return response.json().get("rates", {})
    except Exception as e:
        print(f"Ошибка при загрузке валют: {e}")
    return {}

def get_currency_codes():
    """Извлекает только список доступных кодов (USD, EUR, RUB и т.д.)."""
    rates = get_currency_data("USD")
    return sorted(rates.keys()) if rates else[]

def calculate_exchange(amount, from_v, to_v):
    """Запрашивает курс и производит расчет конвертации."""
    rates = get_currency_data(from_v)
    rate = rates.get(to_v)
    if rate:
        res_val = float(amount) * rate
        return f"{res_val:.2f}"
    return "Ошибка расчета"