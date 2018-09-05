import os
import yaml
import sys

with open("app.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except Exception as e:
        sys.exit(str(e))


def _get_config_value(key, default_value):
    return os.environ.get(key, config.get(key, default_value))


class Config(object):

    UPLOAD_IMAGE = _get_config_value('UPLOAD_FOLDER', 'UPLOAD_IMAGE')
    EDIT_IMAGE = _get_config_value('EDIT_IMAGE', 'EDIT_IMAGE')
    ALLOWED_EXTENSIONS = _get_config_value('ALLOWED_EXTENSIONS',
                                           ['img', 'jpeg', 'jpg', 'png'])
    CONTENT_TYPE = _get_config_value('CONTENT_TYPE',
                                     ['image/jpeg', 'image/jpg', 'image/png'])
    #SECRET_KEY = _get_config_value('SECRET_KEY',
                                   #'b594481f-f3b2-49d0-9fc6-29c1d0859d2e')
    #SQLALCHEMY_DATABASE_URI = _get_config_value(
        #'SQLALCHEMY_DATABASE_URI',
        #'mysql://dt_admin:dt_admin@localhost/avatar')


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False


class StagingConfig(Config):

    pass


class TestingConfig(Config):

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig
}
