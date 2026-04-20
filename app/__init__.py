from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from app.manager import bp as manager_bp
from app.auth import bp as auth_bp



# Инициализируем расширения без привязки к конкретному app
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'  # Куда перенаправлять неавторизованных
login.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(name)
    app.config.from_object(config_class)

    # Привязываем расширения к созданному приложению
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Регистрируем блюпринты
    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.register_blueprint(manager_bp)

    return app