from flask import request
import requests
from datetime import datetime, timedelta

def get_currency_data():
    """Получает список всех доступных кодов валют через er-api."""
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        if response.status_code == 200:
            return sorted(response.json().get("rates", {}).keys())
    except Exception as e:
        print(f"Ошибка при загрузке валют: {e}")
    return[]

def process_exchange_dashboard():
    """Готовит данные для дашборда с курсами и историей."""
    
    items = get_currency_data()
    
    selected_base = request.args.get('base_currency', 'USD')
    selected_target = request.args.get('target_currency', 'EUR')
    selected_period = request.args.get('period', '1y') 
    
    current_rate = "Ошибка"
    high_rate = "-"
    low_rate = "-"
    chart_data =[]

    if selected_base == selected_target:
        return {
            "items": items, "selected_base": selected_base, "selected_target": selected_target,
            "selected_period": selected_period, "current_rate": "1.0000",
            "high_rate": "1.0000", "low_rate": "1.0000", "chart_data":[]
        }

    # --- ИЗБАВЛЯЕМСЯ ОТ IF/ELSE С ПОМОЩЬЮ СЛОВАРЯ ---
    period_days = {
        '1mo': 30,
        '6mo': 180,
        '1y': 365,
        '5y': 5 * 365,
        '10y': 10 * 365
    }

    # Получаем количество дней по ключу (если пришел кривой период, по умолчанию берем 365)
    days_to_subtract = period_days.get(selected_period, 365)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_to_subtract)

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    try:
        # Текущий курс
        url_current = f"https://open.er-api.com/v6/latest/{selected_base}"
        resp_curr = requests.get(url_current, timeout=5)
        if resp_curr.status_code == 200:
            rate = resp_curr.json().get("rates", {}).get(selected_target)
            if rate:
                current_rate = f"{rate:.4f}"

        # История для графика
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
        print(f"Ошибка при работе с API: {e}")

    return {
        "items": items,
        "selected_base": selected_base,
        "selected_target": selected_target,
        "selected_period": selected_period,
        "current_rate": current_rate,
        "high_rate": high_rate,
        "low_rate": low_rate,
        "chart_data": chart_data
    }