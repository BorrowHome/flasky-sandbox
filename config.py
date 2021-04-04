from waitress_manage import basedir


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = basedir + "\\app\\static\\video\\"
    ALLOWED_EXTENSIONS = set(['mp4'])  # @hehao
    UPLOAD_IMAGE_PATH = basedir + "\\app\\static\\image\\"
    SAVE_DOCUMENT_PATH = basedir + "\\app\\static\\document\\"
    SAVE_VIDEO_PATH = basedir + "\\app\\static\\video\\"
    LINER_CONFIG = {
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
