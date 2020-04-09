# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

# db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    # print (config_name, '   config_name ')
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = '123456'
    config[config_name].init_app(app)
    # TODO  liliangbin  路由与自定义错误页面
    bootstrap = Bootstrap(app)

    # 预测情况我们都用init_app函数来初始化，但是好像有问题，但是构造函数好像还可以自动的生成，应该不是问题
    # db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
