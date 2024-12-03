class Config:
    SECRET_KEY = 'sua_chave_secreta_aqui'
    SECURITY_PASSWORD_SALT = 'sua_salt_secreta_aqui'
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_TIMEOUT = 5  # em minutos

    # Configurações de e-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'testeredesdistribuidas@gmail.com'
    MAIL_PASSWORD = 'bsqh jccy mcrm rnxx'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}