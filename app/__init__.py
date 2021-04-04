# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import *


#  临时方案 此时base dir在temp 目录下

def create_app(basedir):
    app = Flask(__name__, static_folder=basedir + '\\app\\static', static_url_path="/static/")
    print('current ===> ' + basedir)
    CORS(app, resources=r'/*')
    # print (config_name, '   config_name ')
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
