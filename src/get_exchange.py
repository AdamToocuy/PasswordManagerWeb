import requests

# URL для получения списка валют и курсов (база USD для получения всех кодов)
API_URL = "https://open.er-api.com/v6/latest/USD"

def get_currency_data():
    """Получает список всех доступных кодов валют."""
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Извлекаем только коды валют из ключей словаря 'rates'
            return sorted(data.get("rates", {}).keys())
    except Exception as e:
        print(f"Ошибка при загрузке валют: {e}")
    return []

def calculate_exchange(amount, from_v, to_v):
    """Запрашивает курс и производит расчет конвертации."""
    try:
        conv_url = f"https://open.er-api.com/v6/latest/{from_v}"
        resp = requests.get(conv_url, timeout=5)
        if resp.status_code == 200:
            conv_data = resp.json()
            rate = conv_data["rates"].get(to_v)
            if rate:
                res_val = float(amount) * rate
                return f"{res_val:.2f}"
    except Exception as e:
        print(f"Ошибка при расчете: {e}")
    return "Ошибка расчета"