from flask import request
import requests
from datetime import datetime, timedelta

# Импортируем функции из вашего файла get_exchange.py
from get_exchange import get_currency_codes, get_currency_data

def process_exchange_dashboard():
    """Готовит данные для дашборда с курсами и историей."""
    
    # 1. Получаем список ВСЕХ доступных валют через get_exchange.py
    items = get_currency_codes()
    
    # 2. Получаем параметры из формы (или задаем по умолчанию)
    selected_base = request.args.get('base_currency', 'USD')
    selected_target = request.args.get('target_currency', 'EUR')
    selected_period = request.args.get('period', '1mo')
    is_rtl = request.args.get('rtl') == '1'
    
    current_rate = "Ошибка"
    high_rate = "-"
    low_rate = "-"
    chart_data =[]

    # 3. Запрашиваем актуальные курсы через get_exchange.py
    rates = get_currency_data(selected_base)
    rate = rates.get(selected_target)
    if rate:
        current_rate = f"{rate:.4f}"

    # Если валюты одинаковые (например, USD в USD), график строить бессмысленно
    if selected_base == selected_target:
        current_rate = "1.0000"
        high_rate = "1.0000"
        low_rate = "1.0000"
    else:
        # --- ИЗБАВЛЯЕМСЯ ОТ IF/ELSE С ПОМОЩЬЮ СЛОВАРЯ ---
        period_days = {
            '1mo': 30,
            '6mo': 180,
            '1y': 365,
            '5y': 5 * 365,
            '10y': 10 * 365
        }
        days_to_subtract = period_days.get(selected_period, 30)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_to_subtract)

        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        # Запрашиваем историю для графика (через API Frankfurter)
        try:
            url_hist = f"https://api.frankfurter.app/{start_str}..{end_str}?from={selected_base}&to={selected_target}"
            resp_hist = requests.get(url_hist, timeout=5)
            
            if resp_hist.status_code == 200:
                rates_history = resp_hist.json().get("rates", {})
                vals =[]
                
                for date_key, rate_dict in rates_history.items():
                    hist_val = rate_dict.get(selected_target)
                    if hist_val:
                        dt_obj = datetime.strptime(date_key, "%Y-%m-%d")
                        ts = int(dt_obj.timestamp() * 1000)
                        chart_data.append([ts, round(hist_val, 4)])
                        vals.append(hist_val)
                        
                if vals:
                    high_rate = f"{max(vals):.4f}"
                    low_rate = f"{min(vals):.4f}"
            else:
                print("Исторические данные недоступны для этой пары.")
                
        except Exception as e:
            print(f"Ошибка при работе с API Frankfurter: {e}")

    # 4. Строим тот самый DASHBOARD для вёрстки
    dashboard = {
        "cards":[
            {
                "title": f"Курс ({selected_base} → {selected_target})",
                "value": current_rate,
                "color": "text-primary",
                "badge": "Сейчас",
                "badge_color": "bg-primary"
            },
            {
                "title": "Максимум за период",
                "value": high_rate,
                "color": "text-success",
                "badge": "MAX",
                "badge_color": "bg-success"
            },
            {
                "title": "Минимум за период",
                "value": low_rate,
                "color": "text-danger",
                "badge": "MIN",
                "badge_color": "bg-danger"
            }
        ]
    }

    # 5. Возвращаем всё, что требует exchange_rates.html
    return {
        "items": items,
        "selected_base": selected_base,
        "selected_target": selected_target,
        "selected_period": selected_period,
        "is_rtl": is_rtl,
        "dashboard": dashboard, 
        "chart_data": chart_data
    }