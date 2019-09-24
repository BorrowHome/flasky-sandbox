# -*- coding: utf-8 -*-

import os
import time

from flask import render_template

from . import main
from .. import db
from ..models import User


@main.route('/')
def index():
    # 这里的主入口是我们函数的dir 最好用绝对路径，临时用相对路径
    video_names = []
    path_in = './app/static'
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in filenames:
            # dir_file_name = os.path.join(dirpath, filename)
            dir_file_name = filename
            if os.path.splitext(dir_file_name)[1] == '.mp4':  # (('./app/static/movie', '.mp4'))
                print(dir_file_name)
                video_names.append(dir_file_name)

    return render_template('index.html', video_names=video_names, site_left_top='33.33,33.33',
                           site_left_bottom='33.33,64.39',
                           site_right_top='78.33,64.39', site_right_bottom='78.33,67.33')


@main.route('/query')
def query():
    user = User()
    user.username = 'user_name_test' + str(time.time())
    db.session.add(user)
    db.session.commit()
    print('commit')
    return render_template('web_wideo.html')
