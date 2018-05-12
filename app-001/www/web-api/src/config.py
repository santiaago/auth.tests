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
    FACEBOOK_OAUTH_CLIENT_ID = getenv('FACEBOOK_OAUTH_CLIENT_ID', False)
    FACEBOOK_OAUTH_CLIENT_SECRET = getenv('FACEBOOK_OAUTH_CLIENT_SECRET', False)

class ProductionConfig(Config):
    PROD = True
    DEBUG = False
    VERSION = 'v1.0'
    FACEBOOK_OAUTH_CLIENT_ID = getenv('FACEBOOK_OAUTH_CLIENT_ID')
    FACEBOOK_OAUTH_CLIENT_SECRET = getenv('FACEBOOK_OAUTH_CLIENT_SECRET')


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
