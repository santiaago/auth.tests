from os import getenv

class Config(object):
    '''
    Base class for application configuration details.
    '''
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    PROD = False
    DEBUG = True
    VERSION = 'v0.0 dev'

class ProductionConfig(Config):
    PROD = True
    DEBUG = False
    VERSION = 'v1.0'

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
