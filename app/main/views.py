# -*- coding: utf-8 -*-

import base64
import os
import time

import cv2
import numpy as np
from flask import render_template, request

from app.utils.sublow import PictureSub
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


@main.route('/query/')
def query():
    user = User()
    user.username = 'user_name_test' + str(time.time())
    db.session.add(user)
    db.session.commit()
    print('commit')
    return render_template('web_wideo.html')


@main.route('/canvas/')
def img_to_canvas():
    return render_template('viedo.html')


@main.route('/picture/', methods=['GET', 'POST'])
def picture():
    # TODO 2019/10/1 12:02 liliangbin  当前帧解码 ，并调用图像处理函数  返回一个字符串
    # 输入的base64编码字符串必须符合base64的padding规则。“当原数据长度不是3的整数倍时, 如果最后剩下两个输入数据，在编码结果后加1个“=”；
    # 如果最后剩下一个输入数据，编码结果后加2个“=”；如果没有剩下任何数据，就什么都不要加，这样才可以保证资料还原的正确性。”
    #

    if request.method == 'POST':
        str = request.form['current_frame']
        str = str.split(',')[1]

        #  在逗号以后的才是编码数据 前面是协议和格式
        if (len(str) % 3 == 1):
            str += "=="
        elif (len(str) % 3 == 2):
            str += "="

        image = base64.b64decode(str)
        np_array = np.fromstring(image, np.uint8)
        # 生成cv2 需要的数据类型
        img_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        cv2.imwrite("test2.png", img_np)
        # INFO 2019/10/1 20:16 liliangbin  返回一个给echart 使用的数据类型，这个地方需要再瞅瞅

        res = {}
        sub = PictureSub()

        # 背景图
        background = cv2.imread('E:/frame/back.png')
        currentFrame = img_np
        # currentFrame = cv2.imread('E:/frame/17316.jpg')

        q = sub.subtract_demo(background, currentFrame)
        s = sub.inverse(q)
        t = sub.iblack(s, 220)
        s = sub.isblack(t, 240)
        res = sub.ipaint(s, 50)

        return res


@main.route('/site/', methods=['GET', 'POST'])
def site():
    if request.method == 'POST':
        print("post")
        print(request.form)
        left_1 = request.form['site_left_top']
        left_2 = request.form['site_left_bottom']
        right_1 = request.form['site_right_top']
        right_2 = request.form['site_right_bottom']
        print(left_1, left_2, right_1, right_2)
        return left_1
    else:
        print("done")

    return "done"
