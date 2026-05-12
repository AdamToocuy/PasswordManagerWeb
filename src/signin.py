from data import db_session
from data.users import User

def process_signin(email, password):
    """
    Алгоритм входа в аккаунт.
    Возвращает кортеж: (success: bool, message: str, category: str, user_id: int или None)
    """
    # 1. Проверить наличие всех значений
    if not email or not password:
        return False, 'Пожалуйста, заполните все поля', 'danger', None

    # Нормализуем почту (как мы делали при регистрации для защиты от багов)
    email = email.lower().strip()

    # 2 и 3. Прочитать базу данных и найти нужную почту
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()

    # Если пользователя с такой почтой нет в базе
    if not user:
        return False, 'Пользователь с такой почтой не найден', 'danger', None

    # 4 и 5. "Расхешировать" и сравнить пароли
    # Функция check_password сама захеширует введенный пароль и сравнит его с базой
    if not user.check_password(password):
        return False, 'Неверный пароль', 'danger', None

    # 6. Вход успешен! Возвращаем ID пользователя, чтобы сохранить его в браузере
    return True, 'Вы успешно вошли в систему!', 'success', user.id