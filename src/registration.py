from data import db_session
from data.users import User

def process_registration(email, password, password_confirm):
    """
    Алгоритм регистрации.
    Возвращает кортеж: (success: bool, message: str, category: str)
    """
    # 1. Проверить наличие всех значений
    if not email or not password or not password_confirm:
        return False, 'Пожалуйста, заполните все поля', 'danger'

    # === ИСПРАВЛЕНИЕ БАГА ===
    # Приводим email к нижнему регистру и удаляем пробелы по краям.
    # Делаем это ДО обращения к базе данных.
    email = email.lower().strip()

    # 2. Сравнить пароли
    if password != password_confirm:
        return False, 'Пароли не совпадают!', 'danger'

    # 3. Прочитать базу данных и выявить отсутствие совпадений (почты)
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == email).first():
        return False, 'Такой пользователь уже существует', 'danger'

    # 4 и 5. Создаем пользователя, хешируем пароль и записываем в БД
    user = User(email=email)
    user.set_password(password)

    db_sess.add(user)
    db_sess.commit()

    return True, 'Регистрация прошла успешно! Теперь вы можете войти.', 'success'