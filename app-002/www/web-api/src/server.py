'web api for server'

import logging
import traceback
from os import getenv

from time import strftime

from flask import Flask
from flask import request
from flask import session
from flask import current_app

from flask_caching import Cache

from flask_login import LoginManager

from database.fake_database import FakeDatabase

import config

app = Flask('app')
app.secret_key = 'a secret'
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

import controllers.auth as controllers_auth
import controllers.versions as controllers_versions

config_name = getenv('FLASK_CONFIG', 'dev')

if not config_name in config.config:
    raise ValueError('Invalid FLASK_CONFIG "{}", choose one of {}'.format(
        config_name,
        str.join(', ', config.config.keys())))

app.config.from_object(config.config[config_name])
config.config[config_name].init_app(app)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

login_manager = LoginManager(app)
login_manager.login_view = '/'

controllers_auth.init_auth_controller(app, login_manager)

app.add_url_rule('/api/version', view_func = controllers_versions.get_version, methods=['GET'])

@app.before_first_request
def init_database():
    app.logger.info('init database')
    db = current_app.cache.get('db')
    if db is None:
        app.logger.info('setting database in cache')
        current_app.cache.set('db', FakeDatabase())

@app.after_request
def after_request(response):
    if response.status_code == 500:
        return response

    ts = strftime('[%Y-%b-%d %H:%M]')
    app.logger.info('%s %s %s %s %s %s',
                    ts,
                    request.remote_addr,
                    request.method,
                    request.scheme,
                    request.full_path,
                    response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return "Internal Server Error", 500

if app.config['PROD']:
    app.logger.info('starting server in production mode')
else:
    app.logger.info('starting server in development mode')
