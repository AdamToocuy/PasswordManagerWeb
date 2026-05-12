from flask import Flask, render_template, request, redirect, flash, session

from data.users import User
from converter import process_converter
from exchange_rates import process_exchange_dashboard
from get_exchange import get_currency_data
from data import db_session
from registration import process_registration 
from signin import process_signin 



# Создаем приложение
app = Flask(__name__, template_folder="../templates")
app.config['SECRET_KEY'] = 'kakoy_nibud_ochen_sekretny_kluch'

@app.route('/signin.html', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Запускаем наш алгоритм
        success, message, category, user_id = process_signin(email, password)
        
        flash(message, category)

        if success:
            # Осуществляем вход: записываем ID пользователя в сессию браузера
            session['user_id'] = user_id
            
            return redirect('/index.html') 
        else:
            # Ошибка: возвращаем на страницу входа
            return render_template('signin.html')

    return render_template('signin.html')

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
        # Получаем юзернейм из формы
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Передаем username в логику
        success, message, category = process_registration(username, email, password, password_confirm)
        
        flash(message, category)

        if success:
            return redirect('/signin.html')
        else:
            return render_template('registration.html')

    return render_template('registration.html')

# --- НОВЫЙ МАРШРУТ: ПРОФИЛЬ ---
@app.route('/profile')
def profile():
    # Проверяем, есть ли ID пользователя в сессии (авторизован ли он)
    user_id = session.get('user_id')
    
    if user_id:
        # Если авторизован - ищем его в БД
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        
        if user:
            # Передаем флаг True и данные пользователя
            return render_template('profile.html', is_authenticated=True, user=user)
            
    # Если пользователя в сессии нет (не авторизован) - передаем флаг False
    return render_template('profile.html', is_authenticated=False)

# --- НОВЫЙ МАРШРУТ: ВЫХОД ИЗ АККАУНТА ---
@app.route('/logout')
def logout():
    # Удаляем пользователя из сессии браузера
    session.pop('user_id', None)
    flash('Вы успешно вышли из аккаунта', 'info')
    return redirect('/signin.html')

def main():
    db_session.global_init("db/users.db")
    app.run(host='127.0.0.1', port=8080, debug=True)

if __name__ == '__main__':
    main()    