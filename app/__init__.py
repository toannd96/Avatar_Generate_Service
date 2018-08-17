import os
from flask import Flask, request, abort, g, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from session_interface import ItsdangerousSessionInterface
from config import app_config
from flask_migrate import Migrate
from itsdangerous import BadSignature, URLSafeTimedSerializer
from urlparse import urlparse

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(app_config[env])
    app.config['COOKIE_SERIALIZER'] = \
        URLSafeTimedSerializer(app.secret_key,
                               signer_kwargs={'key_derivation': 'hmac'})

    app.session_interface = ItsdangerousSessionInterface()
    db.init_app(app)
    configure_hooks(app)
    migrate = Migrate(app, db)
    from app import models

    from app.views import GetCookies
    api.add_resource(GetCookies, '/cookies')

    from app.views import PictureUpload
    api.add_resource(PictureUpload, '/upload', endpoint='picture')

    from app.views import PictureGenerator
    api.add_resource(
        PictureGenerator, '/avatar/<string:email_md5>', endpoint='user')

    return app


def configure_hooks(app):
    from models import User, Picture

    @app.before_request
    def process_auth_cookie():
        if 'avatar' not in urlparse(request.url).path:
            if 'session' not in request.cookies:
                app.logger.debug('Missing Session Cookie.')
                abort(401, 'Missing authentication info.')
            try:
                serializer = app.config['COOKIE_SERIALIZER']
                user_info = serializer.loads(request.cookies['session'])
                g.email = user_info['email']

            except BadSignature:
                app.logger.debug('Unable to decrypt Session Cookie value: {}'
                                 .format(request.cookies['session']))
                abort(401, 'Invalid Session Cookie.')

            except Exception as e:
                app.logger.debug(e.message)
                abort(401, str(e))
