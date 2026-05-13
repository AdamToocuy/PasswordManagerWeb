from data import db_session
from data.users import User

def process_registration(username, email, password, password_confirm):
    # Проверяем, что заполнено и имя тоже
    if not username or not email or not password or not password_confirm:
        return False, 'Пожалуйста, заполните все поля', 'danger'

    email = email.lower().strip()

    if password != password_confirm:
        return False, 'Пароли не совпадают!', 'danger'

    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == email).first():
        return False, 'Такой пользователь уже существует', 'danger'

    # Сохраняем username в поле name
    user = User(name=username, email=email)
    user.set_password(password)

    db_sess.add(user)
    db_sess.commit()

    return True, 'Регистрация прошла успешно! Теперь вы можете войти.', 'success'