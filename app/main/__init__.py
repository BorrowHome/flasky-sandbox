# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)
# 我们加入我们自定义的路由情况  ,这地方我们自己给定义出来
# 这个地方我们就相当于有一个关于路由的蓝本包，我们同样可以添加更多的蓝本，名字不同main的蓝本

# import errors, views, file_upload  这种方式在于python2.*  中使用，但不适用于python3 系列 

from . import errors, views, file_upload, draw_frame, get_volume
