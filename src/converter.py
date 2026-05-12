from flask import request
from get_exchange import calculate_exchange

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
        result = calculate_exchange(amount=amount, from_v=selected_from, to_v=selected_to)
                
    return {
        "result": result,
        "selected_from": selected_from,
        "selected_to": selected_to,
        "amount": amount
    }