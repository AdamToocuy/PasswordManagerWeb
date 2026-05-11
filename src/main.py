import os
from flask import Flask, render_template

# Импортируем логику из созданных вами файлов
from converter import process_converter
from exchange_rates import process_exchange_dashboard
from get_exchange import get_currency_data
from data import db_session


# Создаем приложение
app = Flask(__name__, template_folder="../templates")

@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def converter_page():
    # Запрашиваем список валют из get_exchange.py
    items = get_currency_data()
    # Вызываем логику конвертера из converter.py
    context = process_converter()
    return render_template('converter.html', items=items, **context)

@app.route('/exchange.html', methods=['GET'])
def exchange_page():
    # Вызываем логику дашборда из exchange_rates.py
    context = process_exchange_dashboard()
    return render_template('exchange_rates.html', **context)
@app.route('/singin.html', methods=['GET', 'POST'])
def singin_form():
    return render_template('singin.html')
@app.route('/registration.html', methods=['GET', 'POST'])
def registration_form():
    return render_template('registration.html')

if __name__ == '__main__':
    print("=== Запуск единого сервера курсов валют ===")
    print("Адрес: http://127.0.0.1:8080")
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1', debug=True)
    