import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_PATH = os.path.dirname(__file__) + "\\app\\static\\video"
    ALLOWED_EXTENSIONS = set(['mp4'])  # @hehao
    UPLOAD_IMAGE_PATH = "./app/static/image/"
    SAVE_DOCUMENT_PATH = "./app/static/document/"
    SAVE_VIDEO_PATH = "./app/static/video/"
    LINER_CONFIG={
        "pp_vx":
            {
                'title': '支撑剂密度和水平速度关系',
                'x': 'pp',
                'y': 'vpx'
            },
        "pp_vy": {
            'title': '支撑剂密度和垂直速度关系',
            'x': 'pp',
            'y': 'vcs'
        },
        "q_vx": {
            'title': '排量和水平速度关系',
            'x': 'q',
            'y': 'vpx'
        },
        "q_vy": {
            'title': '排量和垂直速度关系',
            'x': 'q',
            'y': 'vcs'
        },
        "ua_vx": {
            'title': '压裂液粘度和水平速度关系',
            'x': 'ua',
            'y': 'vpx'
        },
        "ua_vy": {
            'title': '压裂液粘度和垂直速度关系',
            'x': 'ua',
            'y': 'vcs'
        },
        "c_vx": {
            'title': '砂比和水平速度关系',
            'x': 'c',
            'y': 'vpx'
        },
        "c_vy": {
            'title': '砂比和垂直速度关系',
            'x': 'c',
            'y': 'vcs'
        }
    }
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
