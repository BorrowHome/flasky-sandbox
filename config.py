import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_PATH = os.path.dirname(__file__) + "\\app\\static\\video"
    ALLOWED_EXTENSIONS = set(['mp4'])  # @hehao
    UPLOAD_IMAGE_PATH = "./app/static/image/"
    SAVE_DOCUMENT_PATH = "./app/static/document/"

    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVE_DATABASE_URL') or 'mysql://llb:123456@forcebing.top/liliangbin'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                       'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
