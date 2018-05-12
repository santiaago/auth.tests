'authentication controller'

import logging

from flask import redirect
from flask import jsonify
from flask import flash
from flask import session

from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import UserMixin

from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.facebook import facebook

from authentication.whitelist import is_in_whitelist
from authentication.oauth import OAuthSignIn
from authentication.NotAuthorizedException import NotAuthorizedException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AppUser(UserMixin): 
    def __init__(self, id, username):
        self.id = id
        self.fb_uid = id
        self.username = username

def init_auth_controller(app, login_manager):    
    login_manager = login_manager

    fb_key = app.config['FACEBOOK_OAUTH_CLIENT_ID']
    fb_secret = app.config['FACEBOOK_OAUTH_CLIENT_SECRET']

    facebook_bp = make_facebook_blueprint(
        client_id=fb_key,
        client_secret=fb_secret,
        scope=['email'],
        redirect_url="/callback/facebook"
    )

    app.register_blueprint(facebook_bp, url_prefix="/login")


    @login_manager.user_loader
    def load_user(id):
        database = session['db']
        users = database.get_user(id)
        user = None
        if users is not None and users.count() != 0:
            db_user = users[0]
            user = AppUser(
                db_user['fb_uid'],
                db_user['username']
            )
        return user

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route('/callback/<provider>')
    def callback(provider):
        if not current_user.is_anonymous:
            return redirect('/')
        oauth = OAuthSignIn.get_provider(provider)
        social_id, username, email = oauth.callback()
        if social_id is None:
            flash('Authentication failed.')
            return redirect('/')

        resp = facebook.get("/me?fields=id,name,email,picture")

        def dump(obj):
            for attr in dir(obj):
                logger.info("obj.%s = %r" % (attr, getattr(obj, attr)))
        dump(resp)
        logger.info(social_id)
        logger.info(username)
        logger.info(email)
        
        if not is_in_whitelist(email):
            raise NotAuthorizedException(username)

        user = None
        database = session['db']
        users = database.get_user(social_id)
        if users is not None and users.count() != 0:
            user = users[0]

        if not user:
            app.logger.info('create the user and insert it into the database.')
            app.logger.info('profile: %s\n%s\n%s\n',
                            username,
                            social_id,
                            '')

            user = {
                'username': username,
                'fb_uid': social_id,
                'fb_access_token': ''
            }

            database.insert_user(user)

        # update fb access token to null
        elif len(user['fb_access_token']) > 0:
            app.logger.info('existing user, update the access token to null')
            user['fb_access_token'] = ''

        login_user(AppUser(social_id, username), True)
        return redirect('/')

    @app.route('/api/username')
    @login_required
    def get_username():
        try:
            oauth = OAuthSignIn.get_provider('facebook')
            social_id, username, email = oauth.callback()
            resp = facebook.get("/me?fields=id,name,email,picture")

            def dump(obj):
                for attr in dir(obj):
                    logger.info("obj.%s = %r" % (attr, getattr(obj, attr)))
            dump(resp)

            if resp.status_code != 200:
                logout_user()
                return 'Unauthorized', 401
            return jsonify({'username': username})
        except Exception as ex:
            logger.info('failed to get username for current user %s', ex)
            raise ex
