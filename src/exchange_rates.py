from flask import request
from functools import lru_cache
import yfinance as yf 

from get_exchange import get_currency_codes, get_currency_data

# === НОВАЯ ФУНКЦИЯ ДЛЯ ИСТОРИИ (Берет данные с биржи Yahoo Finance) ===
@lru_cache(maxsize=128)
def fetch_yfinance_history(base, target, period):
    try:
        # Формат тикера для валют в Yahoo Finance: USDRUB=X
        ticker = f"{base}{target}=X"
        
        # Периоды yfinance идеально совпадают с нашими: 1mo, 6mo, 1y, 5y, 10y
        data = yf.Ticker(ticker).history(period=period)
        
        if data.empty:
            return []
            
        chart_data =[]
        for date, row in data.iterrows():
            ts = int(date.timestamp() * 1000)
            chart_data.append([ts, round(row['Close'], 4)])
            
        return chart_data
    except Exception as e:
        print(f"Ошибка yfinance: {e}")
        return[]

def process_exchange_dashboard():
    """Готовит данные для дашборда с курсами и историей."""
    
    items = get_currency_codes()
    selected_base = request.args.get('base_currency', 'USD')
    selected_target = request.args.get('target_currency', 'EUR')
    selected_period = request.args.get('period', '1mo')
    is_rtl = request.args.get('rtl') == '1'
    
    current_rate_str = "Ошибка"
    current_rate_float = 0.0
    high_rate = "-"
    low_rate = "-"
    chart_data =[]

    # 1. Текущий курс
    rates = get_currency_data(selected_base)
    rate = rates.get(selected_target)
    if rate:
        current_rate_float = float(rate)
        current_rate_str = f"{current_rate_float:.4f}"

    if selected_base == selected_target:
        current_rate_str = "1.0000"
        high_rate = "1.0000"
        low_rate = "1.0000"
    else:
        # 2. Получаем НАСТОЯЩУЮ историю с биржи!
        chart_data = fetch_yfinance_history(selected_base, selected_target, selected_period)
        
        # Если данные получены успешно
        if chart_data:
            vals = [point[1] for point in chart_data]
            high_rate = f"{max(vals):.4f}"
            low_rate = f"{min(vals):.4f}"
        
        # 3. Резервная заглушка (если совсем экзотическая валюта, которой нет на бирже)
        if not chart_data and current_rate_float > 0:
            period_days = {'1mo': 30, '6mo': 180, '1y': 365, '5y': 5 * 365, '10y': 10 * 365}
            days_to_subtract = period_days.get(selected_period, 30)
            
            # Устанавливаем разумный лимит точек для заглушки
            points_count = min(days_to_subtract, 100) 
            now_ts = int(datetime.now().timestamp() * 1000)
            step_ms = int((days_to_subtract / points_count) * 24 * 60 * 60 * 1000)
            
            mock_rate = current_rate_float
            vals =[]
            
            for i in range(points_count, -1, -1):
                ts = now_ts - (i * step_ms)
                chart_data.append([ts, round(mock_rate, 4)])
                vals.append(mock_rate)
                # Очень легкое колебание
                mock_rate *= (1 + random.uniform(-0.002, 0.002))
                
            high_rate = f"{max(vals):.4f}"
            low_rate = f"{min(vals):.4f}"

    # Собираем дашборд
    dashboard = {
        "cards":[
            {"title": f"Курс ({selected_base} → {selected_target})", "value": current_rate_str, "color": "text-primary", "badge": "Сейчас", "badge_color": "bg-primary"},
            {"title": "Максимум", "value": high_rate, "color": "text-success", "badge": "MAX", "badge_color": "bg-success"},
            {"title": "Минимум", "value": low_rate, "color": "text-danger", "badge": "MIN", "badge_color": "bg-danger"}
        ]
    }

    return {
        "items": items,
        "selected_base": selected_base,
        "selected_target": selected_target,
        "selected_period": selected_period,
        "is_rtl": is_rtl,
        "dashboard": dashboard, 
        "chart_data": chart_data
    }