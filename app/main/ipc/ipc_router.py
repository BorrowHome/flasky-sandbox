import csv

import numpy as np
from flask import request, Response, render_template

from app.main import main
from app.utils.frame.site import Site
from app.utils.ipc.camera_host import VideoCamera
from app.utils.ipc.li_onvif import Onvif_hik
from app.utils.ipc.multi_thread import myThread, threadsPool
from config import Config


def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@main.route('/steam/')
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
        print('ip 未找到')
        return "ip 未找到"


@main.route('/ipc/')
def ipc():
    ips = []

    path_in = './app/static/video/'
    path_out = '../static/video/'
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    with open(document_path + "ipcConfig.txt", "r+") as  f:
        a = f.readlines()
    for i in a:
        ips.append(i)

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
    with open(document_path + "video_save_location.txt", "r+") as  f:
        a = f.readline()
        a = a.strip()
    print(a)
    return render_template('ipc.html',
                           ips=ips,
                           site_left_top=site_left_top,
                           site_left_bottom=site_left_bottom,
                           site_right_top=site_right_top,
                           site_right_bottom=site_right_bottom,
                           default_ip=ips[0],
                           video_save_location=a
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

        with open(document_path + "site_" + '0' + ".txt", "r+") as  f:
            a = f.readlines()
            print(a)
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))

        res = {}
        llistx = []
        llisty = []
        with open(document_path + 'sand_2.csv', 'r') as f:
            reader = csv.reader(f)

            for i in reader:
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


@main.route('/thread/')
def thread():
    # 创建新线程
    ipv4 = request.args.get('ip')
    if threadsPool.get(ipv4) is not None:
        return ipv4 + '已录制准备'

    ipc = Onvif_hik(ipv4, 8899, 'admin', '')
    print(ipv4)
    if ipc.content_cam():
        rtsp_uri = ipc.get_steam_uri()
        print("get rtsp done")

        thread1 = myThread(1, 'new Thread ' + ipv4, rtsp_uri, ipv4)

        # 开启新线程
        thread1.start()
        threadsPool.__setitem__(ipv4, thread1)

        return ipv4 + '已新建录制'
    else:
        print('ip has some errors')
        return 'ip has some errors'


@main.route('/stop/')
def stop():
    ip = request.args.get('ip')
    print(ip)
    result = threadsPool.get(ip)
    if result == None:
        print('change ExitFlag')
        return '该ip并没有在后台执行录制程序'
    else:
        try:
            print(type(result))
            result.stop()
            threadsPool.__delitem__(ip)
            return '已停止' + ip + '的录制'
        except Exception as e:
            print('停止录制线程出现问题')
            return '录制出现问题'
