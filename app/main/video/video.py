# -*- coding: utf-8 -*-

import csv
import json
import os
import numpy as np
import cv2
from flask import jsonify
from flask import request

from app.main import main
from app.utils.FormutaCount import formuta
from app.utils.frame.frame import base64_to_png
from app.utils.frame.site import Site
from app.utils.frame.sub import PictureSub
from config import Config
from app.utils.image import image_crop, image_split


@main.route('/')
def index():
    # 这里的主入口是我们函数的dir 最好用绝对路径，临时用相对路径
    # 使用url_for的时候使用的是函数名（路由名和函数名应一样。）
    video_names = []
    path_in = './app/static/video/'
    document_path = Config.SAVE_DOCUMENT_PATH
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in filenames:
            # dir_file_name = os.path.join(dirpath, filename)
            dir_file_name = filename
            if os.path.splitext(dir_file_name)[1] == '.mp4' or '.avi':  # (('./app/static/movie', '.mp4'))
                print(dir_file_name)
                video_names.append(dir_file_name)

    if len(video_names):
        video_name = video_names[0].split('.mp4')[0]
    else:
        video_name = '0'
    frame_location = Site.read_site(document_path + "site_{}.txt".format(video_name))
    video_src = video_names[0]
    return jsonify(
        {
            'video_names': video_names,
            'site': frame_location.get_site(),
            'video_src': video_src
        }
    )


@main.route('/picture/', methods=['POST'])
def picture():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    # 传入的当前的帧保存
    data = json.loads(request.get_data(as_text=True))
    str = data.get('current_frame')
    video_name = data.get('video_name').strip()
    img_np = base64_to_png(str)
    image_name = "current_{}.png".format(video_name.strip())
    cv2.imencode('.png', img_np)[1].tofile(image_path + image_name)
    # 保存完毕

    currentFrame = img_np

    sub = PictureSub()
    # # 图像相减
    q = sub.subtract_demo('', currentFrame)
    # # 图像第三通道 反转
    # s = sub.inverse(q)
    #
    # # cv2.imwrite(image_path + "iblack_" + id + ".png", t)
    #
    print(q)
    # cv2.imwrite(image_path + "ipaint_" + video_name + ".png", q)
    cv2.imencode('.png', q)[1].tofile(image_path + "ipaint_" + video_name + ".png")
    # s = sub.testf(image_path + image_name, image_path + image_back,video_name)
    # 图像第三通道 反转
    s = sub.inverse(q)

    # cv2.imwrite(image_path + "iblack_" + id + ".png", t)
    cv2.imencode('.png', s)[1].tofile(image_path + "ipaint_" + video_name + ".png")

    with open(document_path + "site_" + video_name + ".txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

    res = sub.ipaint(q, 220, video_name, frame_location.locate_x, frame_location.move_x, frame_location.locate_y,
                     frame_location.move_y)

    res['max'] = frame_location.move_y
    # 变化得y轴
    res['video_name'] = video_name

    return res


# INFO 2019/12/25 15:18 liliangbin  背景图片设置
@main.route('/background/', methods=['GET', 'POST'])
def background():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    jsonData = json.loads(request.get_data(as_text=True))
    frame = jsonData.get('current_frame')
    video_name = jsonData.get('video_name')
    video_name = "back_{}.png".format(video_name.strip())
    print("=====back image name====={}".format(video_name))
    img_np = base64_to_png(frame)
    cv2.imencode('.png', img_np)[1].tofile(image_path + video_name)
    return 'done'


# TODO 2020/1/4 15:13 liliangbin 返回的地址应该是画框的位置（视频名字和时间位置）通过前端设置了
@main.route('/site/', methods=['POST'])
def site():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH

    data = json.loads(request.get_data(as_text=True))
    locate_x = int(float(data.get('locate_x')))
    locate_y = int(float(data.get('locate_y')))
    move_x = int(float(data.get('move_x')))
    move_y = int(float(data.get('move_y')))
    video_name = data.get('video_name').strip()
    print("locate x ======>{}".format(locate_x))
    path = document_path + "site_{}.txt".format(video_name)
    with open(path, 'w', encoding="utf-8") as f:
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
    data = json.loads(request.get_data(as_text=True))
    name = data.get('name').strip()
    frame_location = Site.read_site(document_path + "site_{}.txt".format(name))
    return jsonify({'site': frame_location.get_site()})


@main.route('/video_location/', methods=['POST'])
def video_location():
    document_path = Config.SAVE_DOCUMENT_PATH

    video_save_location = request.form.get('video_location')
    location = request.args.get('location')
    print(video_save_location)
    print(location)
    with open(document_path + "video_save_location.txt", 'w') as f:
        f.write(str(video_save_location))


@main.route("/formuta/", methods=['POST'])
def formuta_count():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    pp = data.get('pp')
    pf = data.get('pf')
    dp = data.get('dp')
    ua = data.get('ua')
    c = data.get('c')
    w = data.get('w')
    test_q = data.get('q')
    h = data.get('h')
    fai = data.get('fai')

    print(data)
    # aasd = formuta(pp, pf, dp, ua, c, w, q, h, fai)
    # aasd = formuta(2850, 1020, 0.001, 10, 0.3, 4.5 * 0.001, 5 / 60, 1, 0.3)
    aasd = formuta(pp, pf, dp, ua, c, w, test_q, h, fai)

    q = aasd.Count()

    data.update(q)
    return jsonify(data)


# mosaicpicture

#
@main.route('/mosaicpicture/', methods=['POST'])
def mosaicpicture():
    video_names = []
    image_path = Config.UPLOAD_IMAGE_PATH
    path_in = './app/static/video/'
    document_path = Config.SAVE_DOCUMENT_PATH
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in filenames:
            # dir_file_name = os.path.join(dirpath, filename)
            dir_file_name = filename
            if os.path.splitext(dir_file_name)[1] == '.mp4' or '.avi':  # (('./app/static/movie', '.mp4'))
                print(dir_file_name)
                video_names.append(dir_file_name)
    data = json.loads(request.get_data(as_text=True))
    strqwe = data.get('current_frame')
    video_name = data.get('video_name').strip()
    print(video_names)
    print(video_name)
    for i in range(len(video_names)):
        video_names[i] = video_names[i].split('.mp4')[0]
    videoOrder = video_names.index(video_name)
    CoordinateAddNumb = 0
    # 将超过总的 move_x 的坐标点删除 保证不会出现上次实验留下的多余点
    # 计算最大y数据 MaxY
    MaxY = 0
    for i in video_names:
        frame_location = Site.read_site(document_path + "site_{}.txt".format(i))
        CoordinateAddNumb += frame_location.move_x
        if frame_location.move_y > MaxY:
            MaxY = frame_location.move_y

    with open(document_path + "sand_VideoMosaic.csv", "r+") as  f:
        qwe = f.read().strip().split('\n')
        Lenqwe = len(qwe)
        if Lenqwe < CoordinateAddNumb + 10:
            for i in range(CoordinateAddNumb + 10 - Lenqwe):
                qwe.append('{},0'.format(Lenqwe + i))
        qwe = qwe[0:CoordinateAddNumb + 10]
    with open(document_path + "sand_VideoMosaic.csv", "w+") as f:
        f.writelines('\n'.join(qwe))

    CoordinateAddNumb = 0
    for i in video_names[0:videoOrder]:
        frame_location = Site.read_site(document_path + "site_{}.txt".format(i))
        CoordinateAddNumb += frame_location.move_x
    frame_location = Site.read_site(document_path + "site_{}.txt".format(video_name))
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    # 传入的当前的帧保存
    # video_name = data.get('video_name').strip()
    img_np = base64_to_png(strqwe)
    image_name = "current_{}.png".format(video_name.strip())
    cv2.imencode('.png', img_np)[1].tofile(image_path + image_name)
    # 保存完毕
    # 当前帧减去背景帧
    currentFrame = img_np
    sub = PictureSub()
    # 图像相减
    q = sub.subtract_demo('', currentFrame)
    # 图像第三通道 反转
    s = sub.inverse(q)
    cv2.imencode('.png', s)[1].tofile(image_path + "ipaint_" + video_name + ".png")
    with open(document_path + "site_" + video_name.strip() + ".txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    print(video_name)
    res = sub.ipaint(q, 220, video_name, frame_location.locate_x, frame_location.move_x, frame_location.locate_y,
                     frame_location.move_y)
    # res 进行处理
    # 调整拼接视频数据csv 对应位置的值
    for i in range(len(res['list_x'])):
        res['list_x'][i] = res['list_x'][i] + CoordinateAddNumb

    with open(document_path + "sand_VideoMosaic.csv", "r+") as  f:
        qwe = f.read().strip().split('\n')
        writer = csv.writer(f)
        print(len(res['list_x']), len(res['list_y']))
        for i in range(len(res['list_x'])):
            qwe[CoordinateAddNumb + i] = qwe[CoordinateAddNumb + i].split(',')[0] + ',{}'.format(res['list_y'][i])
    with open(document_path + "sand_VideoMosaic.csv", "w+") as  f:
        f.writelines('\n'.join(qwe))
    listx = []
    listy = []
    # 根据拼接视频csv 上传res数据
    with open(document_path + "sand_VideoMosaic.csv", "r+") as  f:
        wadad = f.read().strip().split('\n')
        for i in wadad:
            listx.append(int(i.split(',')[0]))
            listy.append(int(i.split(',')[1]))
    res = {
        "list_x": listx,
        "list_y": listy
    }
    res['max'] = MaxY
    # 变化得y轴
    res['video_name'] = video_name
    # 以下为拼接图片显示区域
    imagenames = []
    print(video_names)
    if videoOrder == len(video_names) - 1:
        for i in video_names:
            image_path = './app/static/image/'
            image_crop(image_path + 'current_{}.png'.format(i), document_path + 'site_{}.txt'.format(i), image_path + i)
        imagenames = [image_path + i + '_mosaic.jpg' for i in video_names]
        image_split(image_path, imagenames, len(video_names))

    # 添加  用于增加当前视频显示在图标中的坐标值
    return res
