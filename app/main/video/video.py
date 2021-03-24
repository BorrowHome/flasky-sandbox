# -*- coding: utf-8 -*-

import csv
import json
import os

import cv2
from flask import jsonify
from flask import request

from app.main import main
from app.utils.FormutaCount import formuta
from app.utils.frame.frame import base64_to_png
from app.utils.frame.site import Site
from app.utils.frame.sub import PictureSub
from config import Config


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
        video_name = video_names[0].split('.')[0]
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
    cv2.imwrite(image_path + image_name, img_np)
    # 保存完毕

    # 当前帧减去背景帧
    image_back = "back_{}.png".format(video_name)
    background = cv2.imread(image_path + image_back)

    currentFrame = img_np

    sub = PictureSub()
    # 图像相减
    q = sub.subtract_demo(background, currentFrame)
    # 图像第三通道 反转
    s = sub.inverse(q)

    # cv2.imwrite(image_path + "iblack_" + id + ".png", t)

    cv2.imwrite(image_path + "ipaint_" + video_name + ".png", s)

    with open(document_path + "site_" + video_name + ".txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

    res = sub.ipaint(s, 220, video_name, frame_location.locate_x, frame_location.move_x, frame_location.locate_y,
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
    cv2.imwrite(image_path + video_name, img_np)
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

    # aasd = formuta(pp, pf, dp, ua, c, w, q, h, fai)
    aasd = formuta(2850, 1020, 0.001, 10, 0.3, 4.5 * 0.001, 5 / 60, 1, 0.3)
    q = aasd.Count()
    data.update(q)
    return jsonify(data)
