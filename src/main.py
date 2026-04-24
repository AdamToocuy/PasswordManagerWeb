from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="../templates")

# URL для получения списка валют и курсов (база USD для получения всех кодов)
API_URL = "https://open.er-api.com/v6/latest/USD"

def get_currency_data():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Извлекаем только коды валют из ключей словаря 'rates'
            return sorted(data.get("rates", {}).keys())
    except Exception as e:
        print(f"Ошибка при загрузке валют: {e}")
    return ["USD", "EUR", "RUB"] # Запасной список

@app.route('/', methods=['GET', 'POST'])
def index():
    # Получаем актуальный список валют из API при каждом (или первом) запросе
    items = get_currency_data()
    result = ""
    selected_from = request.form.get('from_currency', 'USD')
    selected_to = request.form.get('to_currency', 'RUB')
    
    if request.method == 'POST':
        amount = request.form.get('source_amount')
        from_v = request.form.get('from_currency')
        to_v = request.form.get('to_currency')
        
        if amount and from_v and to_v:
            try:
                # Запрашиваем курс относительно выбранной базовой валюты
                conv_url = f"https://open.er-api.com/v6/latest/{from_v}"
                resp = requests.get(conv_url)
                conv_data = resp.json()
                rate = conv_data["rates"].get(to_v)
                
                if rate:
                    res_val = float(amount) * rate
                    result = f"{res_val:.2f}"
            except:
                result = "Ошибка расчета"

    return render_template('index.html', 
                           items=items, 
                           result=result, 
                           selected_from=selected_from, 
                           selected_to=selected_to)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
