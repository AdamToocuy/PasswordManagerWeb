from flask import request
import requests

def process_converter():
    """Логика конвертера валют."""
    result = ""
    selected_from = 'USD'
    selected_to = 'RUB'
    amount = ""
    
    if request.method == 'POST':
        selected_from = request.form.get('from_currency', 'USD')
        selected_to = request.form.get('to_currency', 'RUB')
        amount = request.form.get('source_amount', '')
        
        if amount and selected_from and selected_to:
            try:
                conv_url = f"https://er-api.com{selected_from}"
                resp = requests.get(conv_url, timeout=5)
                if resp.status_code == 200:
                    conv_data = resp.json()
                    rate = conv_data["rates"].get(selected_to)
                    if rate:
                        res_val = float(amount) * rate
                        result = f"{res_val:.2f}"
            except Exception as e:
                print(f"Ошибка конвертера: {e}")
                result = "Ошибка расчета"
                
    return {
        "result": result,
        "selected_from": selected_from,
        "selected_to": selected_to,
        "amount": amount
    }