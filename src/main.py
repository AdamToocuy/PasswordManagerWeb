from flask import Flask, render_template, request, redirect, flash

# Импортируем логику из созданных вами файлов
from converter import process_converter
from exchange_rates import process_exchange_dashboard
from get_exchange import get_currency_data
from data import db_session
from registration import process_registration 


# Создаем приложение
app = Flask(__name__, template_folder="../templates")
app.config['SECRET_KEY'] = 'kakoy_nibud_ochen_sekretny_kluch'


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

@app.route('/registration.html', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # 1. Получить значения из окна ввода
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Вызываем алгоритм из отдельного файла
        success, message, category = process_registration(email, password, password_confirm)
        
        # Показываем сообщение (ошибку или успех)
        flash(message, category)

        # Если регистрация успешна - перенаправляем на вход
        if success:
            return redirect('/signin.html')
        # Если ошибка - возвращаем пользователя на страницу регистрации
        else:
            return render_template('registration.html')

    # GET-запрос (просто открытие страницы)
    return render_template('registration.html')

@app.route('/signin.html')
def signin():
    return render_template('signin.html')

def main():
    db_session.global_init("db/users.db")
    app.run(debug=True)

if __name__ == '__main__':
    main()    