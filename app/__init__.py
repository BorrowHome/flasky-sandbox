# -*- coding: utf-8 -*-

from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
from flask_socketio import SocketIO, emit
from config import config

# db = SQLAlchemy()
socketio = SocketIO()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__, template_folder="./templates", static_folder="./static", static_url_path="/static/")
    CORS(app, resources=r'/*')
    # print (config_name, '   config_name ')
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = '123456'
    app.config['THREADED'] = True
    config[config_name].init_app(app)
    # TODO  liliangbin  路由与自定义错误页面
    socketio.init_app(app)
    bootstrap.init_app(app)
    # 预测情况我们都用init_app函数来初始化，但是好像有问题，但是构造函数好像还可以自动的生成，应该不是问题
    # db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.route('/liliangbin')
    def fsdf():
        return render_template('test.html')

    return app


