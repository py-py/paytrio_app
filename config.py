import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SHOP_KEY = os.environ.get('SECRET_SHOP') or 'Ohd5xw4IHaixSqxHj8YgKgkogToslDZVk'
    SHOP_ID = os.environ.get('ID_SHOP') or '306267'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


class ProductConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductConfig,
    # default development
    'default': DevelopmentConfig,
}
