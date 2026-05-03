from flask import request
# Импортируем функцию запроса данных из вашего файла
from get_exchange import get_currency_data
import requests

def process_exchange_dashboard():
    """
    Получает данные из API и готовит контекст для дашборда exchange_rates.html.
    Поддерживает RTL-логику отображения.
    """
    # 1. Получаем список всех валют для выпадающих списков
    items = get_currency_data()
    
    # 2. Получаем выбранные пользователем валюты (по умолчанию USD и EUR)
    selected_base = request.args.get('base_currency', 'USD')
    selected_target = request.args.get('target_currency', 'EUR')
    
    # Значения по умолчанию для карточек
    current_rate = "1.0000"
    high_rate = "1.0000"
    low_rate = "1.0000"
    chart_data = [1.0] * 7
    
    # 3. Получаем реальный курс через API для выбранной базовой валюты
    try:
        url = f"https://er-api.com{selected_base}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            rates = data.get("rates", {})
            
            rate = rates.get(selected_target)
            if rate:
                current_rate = f"{rate:.4f}"
                # Имитируем небольшие колебания для карточек Максимум/Минимум за 24ч
                high_rate = f"{(rate * 1.005):.4f}"
                low_rate = f"{(rate * 0.995):.4f}"
                
                # Генерируем псевдо-исторические данные для графика за 7 дней
                chart_data = [
                    round(rate * 0.996, 4),
                    round(rate * 1.002, 4),
                    round(rate * 0.991, 4),
                    round(rate * 1.005, 4),
                    round(rate * 0.998, 4),
                    round(rate * 1.003, 4),
                    round(rate, 4)
                ]
    except Exception as e:
        print(f"Ошибка при расчете дашборда: {e}")
        current_rate = "Ошибка"

    # Возвращаем словарь с переменными для Jinja2 в шаблоне
    return {
        "items": items,
        "selected_base": selected_base,
        "selected_target": selected_target,
        "current_rate": current_rate,
        "high_rate": high_rate,
        "low_rate": low_rate,
        "chart_data": chart_data
    }
