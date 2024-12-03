from flask import Flask
from flask_login import LoginManager
from .config import config
from passlib.hash import argon2

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Simulação de um banco de dados de usuários
users = {
    'mo': {
        'password': argon2.hash('mo123'),
        'role': 'super_admin',
        'email': 'moniquedemoraes@hotmail.com',
        'full_name': 'Monique Moraes'
    },
    'admin': {'password': argon2.hash('admin123'), 'role': 'admin', 'email': 'admin@example.com', 'full_name': 'Admin User'},
    'usuario': {'password': argon2.hash('user123'), 'role': 'cliente', 'email': 'user@example.com', 'full_name': 'Regular User'}
}

login_attempts = {}

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    login_manager.init_app(app)

    # Adicione users e login_attempts à configuração do app
    app.config['USERS'] = users
    app.config['LOGIN_ATTEMPTS'] = login_attempts

    # Registre os blueprints
    from .routes import auth, main, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    # Context processor
    @app.context_processor
    def inject_users():
        return dict(users=app.config['USERS'])

    return app