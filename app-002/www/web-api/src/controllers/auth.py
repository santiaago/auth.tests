'authentication controller'

from flask import redirect
from flask import jsonify
from flask import flash
from flask import current_app

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
        redirect_url='/callback/facebook'
    )

    app.register_blueprint(facebook_bp, url_prefix='/login')


    @login_manager.user_loader
    def load_user(id):
        current_app.logger.info('loading user %s', id)
        
        database = current_app.cache.get('db')
        if database is None:
            current_app.logger.error('unable to retrieve database')
            raise Exception('database not found')
        users = database.get_user(id)
        user = None
        if users is not None and len(users) != 0:
            current_app.logger.info('user found')
            db_user = users[0]
            user = AppUser(
                db_user.id,
                db_user.username
            )
        else:
            current_app.logger.info('user not found in database')
        return user

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route('/callback/<provider>')
    def callback(provider):
        current_app.logger.info('callback/provider')
        if not current_user.is_anonymous:
            return redirect('/')
        oauth = OAuthSignIn.get_provider(provider)
        social_id, username, email = oauth.callback()
        if social_id is None:
            flash('Authentication failed.')
            return redirect('/')

        resp = facebook.get('/me?fields=id,name,email,picture')

        def dump(obj):
            for attr in dir(obj):
                current_app.logger.info('obj.%s = %r' % (attr, getattr(obj, attr)))
        dump(resp)
        current_app.logger.info(social_id)
        current_app.logger.info(username)
        current_app.logger.info(email)
        
        if not is_in_whitelist(email):
            raise NotAuthorizedException(username)

        user = None

        database = current_app.cache.get('db')
        users = database.get_user(social_id)
        if users is not None and len(users) != 0:
            user = users[0]

        if not user:
            current_app.logger.info('create the user and insert it into the database.')
            current_app.logger.info('profile: username:%s\nsocial_id:%s\n',
                            username,
                            social_id)

            user = AppUser(social_id, username)

            current_app.logger.info('updating cache with user')
            database.insert_user(user)
            current_app.cache.set('db', database)

        login_user(AppUser(social_id, username), True)
        return redirect('/')

    @app.route('/api/username')
    @login_required
    def get_username():
        try:
            current_app.logger.info('auth.get_username')
            oauth = OAuthSignIn.get_provider('facebook')
            social_id, username, email = oauth.callback()
            current_app.logger.info('from callback id: %s username: %s email: %s',
                social_id,
                username,
                email)
            
            resp = facebook.get('/me?fields=id,name,email,picture')

            def dump(obj):
                'dump object attributes'
                for attr in dir(obj):
                    current_app.logger.info('obj.%s = %r' % (attr, getattr(obj, attr)))

            dump(resp)

            if resp.status_code != 200:
                logout_user()
                return 'Unauthorized', 401
            return jsonify({'username': username})
        except Exception as ex:
            current_app.logger.info('failed to get username for current user %s', ex)
            raise ex
