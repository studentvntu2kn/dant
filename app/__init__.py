from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    # Реєстрація маршрутів
    from .routes import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    from .cabinet import cabinet
    app.register_blueprint(cabinet)

    # Підгрузка користувачів
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app
