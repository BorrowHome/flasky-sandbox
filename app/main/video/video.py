# -*- coding: utf-8 -*-

import csv
import os

import cv2
import numpy as np
from flask import render_template, request, redirect, url_for
from flask import jsonify
from app.main import main
from app.utils.frame.frame import base64_to_png
from app.utils.frame.site import Site
from app.utils.frame.sub import PictureSub
from config import Config
import json


@main.route('/')
def index():
    # 这里的主入口是我们函数的dir 最好用绝对路径，临时用相对路径
    # 使用url_for的时候使用的是函数名（路由名和函数名应一样。）
    video_names = []
    path_in = './app/static/video/'
    path_out = 'http://localhost:8082/static/video/'
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in filenames:
            # dir_file_name = os.path.join(dirpath, filename)
            dir_file_name = filename
            if os.path.splitext(dir_file_name)[1] == '.mp4' or '.avi':  # (('./app/static/movie', '.mp4'))
                print(dir_file_name)
                video_names.append(dir_file_name)
    with open(document_path + "site_0.txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    video_src = video_names[0]
    tmp2 = frame_location.locate_y + frame_location.move_y
    tmp1 = frame_location.locate_x + frame_location.move_x
    site_left_top = [str(frame_location.locate_x), str(frame_location.locate_y)]
    site_left_bottom = [str(frame_location.locate_x), str(tmp2)]

    site_right_top = [str(tmp1), str(frame_location.locate_y)]
    site_right_bottom = [str(tmp1), str(tmp2)]

    return jsonify(
        {
            'video_names': video_names,
            'site': {
                'site_left_top': site_left_top,
                'site_left_bottom': site_left_bottom,
                'site_right_top': site_right_top,
                'site_right_bottom': site_right_bottom,
            },
            'video_src': video_src
        }
    )


@main.route('/picture/', methods=['GET', 'POST'])
def picture():
    # TODO 2019/10/1 12:02 liliangbin  当前帧解码 ，并调用图像处理函数  返回一个字符串
    # 输入的base64编码字符串必须符合base64的padding规则。“当原数据长度不是3的整数倍时, 如果最后剩下两个输入数据，在编码结果后加1个“=”；
    # 如果最后剩下一个输入数据，编码结果后加2个“=”；如果没有剩下任何数据，就什么都不要加，这样才可以保证资料还原的正确性。”
    #
    import time
    start = time.clock()
    # 中间写上代码块

    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        str = data.get('current_frame')
        video_name = data.get('video_name')
        imageStart = time.clock()
        img_np = base64_to_png(str)
        cv2.imwrite(image_path + "current_" + video_name + ".png", img_np)
        imageEnd = time.clock()
        print('base64topng: %s Seconds' % (imageEnd - imageStart))
        res = {}
        sub = PictureSub()

        # 背景图
        writeImgeStart = time.clock()
        background = cv2.imread(image_path + "back_" + video_name + ".png")
        print(background.shape)
        writeImgeEnd = time.clock()
        print('WriteImge: %s Seconds' % (writeImgeEnd - writeImgeStart))
        currentFrame = img_np

        print(currentFrame.shape)

        q = sub.subtract_demo(background, currentFrame)
        substractIMRun = time.clock()
        print('substract : %s Seconds' % (substractIMRun - writeImgeEnd))

        s = sub.inverse(q)
        InvserseSTOP = time.clock()
        print('inverse : %s Seconds' % (InvserseSTOP - substractIMRun))

        # t = sub.iblack(s, 220)
        imageRun = time.clock()
        print('iblack: %s Seconds' % (imageRun - InvserseSTOP))

        print('sub starct ALL : %s Seconds' % (imageRun - writeImgeEnd))
        # cv2.imwrite(image_path + "iblack_" + id + ".png", t)

        cv2.imwrite(image_path + "ipaint_" + video_name + ".png", s)
        imageStop = time.clock()
        print('write twoImge: %s Seconds' % (imageStop - imageRun))
        with open(document_path + "site_" + video_name + ".txt", "r+") as  f:
            a = f.readlines()
            print(a)
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

        res = sub.ipaint(s, 220, video_name, frame_location.locate_x, frame_location.move_x, frame_location.locate_y,
                         frame_location.move_y)

        res['max'] = frame_location.locate_y + frame_location.move_y
        # 变化得y轴
        list_y = np.array(res['list_y'])

        data_total = res['max'] - list_y
        max_index = max(data_total.tolist())

        res['list_y'] = data_total.tolist()
        res['max'] = max_index + 20
        res['video_name'] = video_name
        # 以前使用的是jsonify===> 前端使用 data["list_y"]==>有什么区别
        end = time.clock()
        print('Running time: %s Seconds' % (end - start))
        return res


# INFO 2019/12/25 15:18 liliangbin  背景图片设置
@main.route('/background/', methods=['GET', 'POST'])
def background():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        jsonData = json.loads(request.get_data(as_text=True))
        frame = jsonData.get('current_frame')
        video_name = jsonData.get('video_name')
        img_np = base64_to_png(frame)
        cv2.imwrite(image_path + "back_" + video_name + ".png", img_np)

        return 'done'


# TODO 2020/1/4 15:13 liliangbin 返回的地址应该是画框的位置（视频名字和时间位置）通过前端设置了
@main.route('/site/', methods=['GET', 'POST'])
def site():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        print("post")
        print(request.form)
        # 数据识别得的时候最好使用整数实现，int和float的转化有问题，就在计算得时候。脑阔疼
        # 大坑
        locate_x = int(float(request.form['locate_x']))
        locate_y = int(float(request.form['locate_y']))
        move_x = int(float(request.form['move_x']))
        move_y = int(float(request.form['move_y']))
        id = request.form['id']
        print(id, "fdsf")
        with open(document_path + "site_" + id + ".txt", 'w') as f:
            f.write(str(locate_x) + '\n')
            f.write(str(locate_y) + '\n')
            f.write(str(move_x) + '\n')
            f.write(str(move_y) + '\n')

    return "done"


# TODO 2020/6/12 15:50 liliangbin 代码可以优化一波
@main.route('/change_datas/', methods=['GET', 'POST'])
def change_datas():
    # 输入的base64编码字符串必须符合base64的padding规则。“当原数据长度不是3的整数倍时, 如果最后剩下两个输入数据，在编码结果后加1个“=”；
    # 如果最后剩下一个输入数据，编码结果后加2个“=”；如果没有剩下任何数据，就什么都不要加，这样才可以保证资料还原的正确性。”
    s = []
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH

    if request.method == 'POST':
        new = eval(request.form.getlist("current_frame")[0])
        id = request.form['id']
        print(type(new), new)
        # new=[int(new[0]),int(new[1])]
    with open(document_path + "site_" + id + ".txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

    with open(document_path + "sand_" + id + ".csv", "r+", encoding="utf-8", newline="")as f:
        reader = csv.reader(f)
        # writer = csv.writer(f)
        print("正在修改csv文件")
        for i in reader:
            s.append(i)
        for i in s:
            # print(i)
            if str(new[0]) == i[0]:
                s[s.index(i)][1] = str(frame_location.move_y + frame_location.locate_y - new[1])
                break
    with open(document_path + "sand_" + id + ".csv", "w", newline="")as f:
        writer = csv.writer(f)
        for i in s:
            writer.writerow(i)
        print("csv文件修改成功")
        return "true"


# INFO 2020/6/12 15:51 liliangbin  获取用户
@main.route("/site_get/", methods=['GET', 'POST'])
def site_get():
    document_path = Config.SAVE_DOCUMENT_PATH
    res = {}
    if request.method == 'POST':
        id = request.form["id"]
        try:
            with open(document_path + "site_" + id + ".txt", "r+") as  f:
                a = f.readlines()
                print(a)
                frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
        except Exception as e:
            print(e.__cause__)
            print('现在还没有存储该site')
            frame_location = Site(0, 0, 0, 0)
        tmp2 = frame_location.locate_y + frame_location.move_y
        tmp1 = frame_location.locate_x + frame_location.move_x
        res['site_left_top'] = str(frame_location.locate_x) + ',' + str(frame_location.locate_y)
        res['site_left_bottom'] = str(frame_location.locate_x) + ',' + str(tmp2)

        res['site_right_top'] = str(tmp1) + ',' + str(frame_location.locate_y)
        res['site_right_bottom'] = str(tmp1) + ',' + str(tmp2)

        # return redirect(url_for('main.index'))

    return res


@main.route('/video_location/', methods=['POST'])
def video_location():
    document_path = Config.SAVE_DOCUMENT_PATH

    video_save_location = request.form.get('video_location')
    location = request.args.get('location')
    print(video_save_location)
    print(location)
    with open(document_path + "video_save_location.txt", 'w') as f:
        f.write(str(video_save_location))

    if location == 'ipc':
        return redirect(url_for('.ipc'))
    elif location == 'multi_video':
        return redirect(url_for('.multi_ipc_video'))
    return redirect('.')
