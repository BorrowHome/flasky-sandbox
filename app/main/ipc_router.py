import csv

import numpy as np
from flask import request, Response, render_template

from app.utils.li_onvif import Onvif_hik
from app.utils.rtsp import VideoCamera
from app.utils.site import Site
from config import Config
from . import main


def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@main.route('/steam')
def steam():
    ipv4 = request.args.get('ip')
    ipc = Onvif_hik(ipv4, 8899, 'admin', '')
    print(ipv4)
    if ipc.content_cam():
        rtsp_uri = ipc.get_steam_uri()
        print("done")
        return Response(gen(VideoCamera(rtsp_uri)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        # return rtsp_uri

    else:
        return "ip 未找到"


@main.route('/canvas/')
def img_to_canvas():
    return render_template('viedo.html')


@main.route('/ipc/')
def ipc():
    ips = ['192.168.1.10', '192.168.1.10']
    path_in = './app/static/video/'
    path_out = '../static/video/'
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH

    with open(document_path + "site_0.txt", "r+") as  f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

    tmp2 = frame_location.locate_y + frame_location.move_y
    tmp1 = frame_location.locate_x + frame_location.move_x
    site_left_top = str(frame_location.locate_x) + ',' + str(frame_location.locate_y)
    site_left_bottom = str(frame_location.locate_x) + ',' + str(tmp2)

    site_right_top = str(tmp1) + ',' + str(frame_location.locate_y)
    site_right_bottom = str(tmp1) + ',' + str(tmp2)

    return render_template('ipc.html',
                           ips=ips,
                           site_left_top=site_left_top,
                           site_left_bottom=site_left_bottom,
                           site_right_top=site_right_top,
                           site_right_bottom=site_right_bottom,
                           default_ip=ips[0]
                           )


@main.route('/camera/', methods=['GET', 'POST'])
def camera():
    # TODO 2019/10/1 12:02 liliangbin  当前帧解码 ，并调用图像处理函数  返回一个字符串
    # 输入的base64编码字符串必须符合base64的padding规则。“当原数据长度不是3的整数倍时, 如果最后剩下两个输入数据，在编码结果后加1个“=”；
    # 如果最后剩下一个输入数据，编码结果后加2个“=”；如果没有剩下任何数据，就什么都不要加，这样才可以保证资料还原的正确性。”
    #
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        str = request.form['current_frame']
        id = request.form['id']

        with open(document_path + "site_" + id + ".txt", "r+") as  f:
            a = f.readlines()
            print(a)
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

        res = {}
        llistx = []
        llisty = []
        with open(document_path + 'sand_2.csv', 'r') as f:
            reader = csv.reader(f)

            for i in reader:
                print(i[0], i[1])
                llistx.append(i[0])
                llisty.append(i[1])

        res['list_x'] = llistx
        res['list_y'] = llisty

        res['max'] = frame_location.locate_y + frame_location.move_y
        # 变化得y轴
        list_y = np.array(res['list_y']).astype(np.int)

        data_total = res['max'] - list_y
        max_index = max(data_total.tolist())

        res['list_y'] = data_total.tolist()
        res['max'] = max_index + 20
        res['id'] = id
        # 以前使用的是jsonify===> 前端使用 data["list_y"]==>有什么区别
        return res
