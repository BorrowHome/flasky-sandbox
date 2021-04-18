from flask import request, jsonify, Response

from app.main import main
from app.utils.frame.site import Site
from app.utils.ipc.camera_host import VideoCamera
from app.utils.ipc.li_onvif import Onvif_hik
from app.utils.ipc.multi_thread import myThread, threadsPool
from config import Config

emit_thread = {}


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@main.route('/ipc/')
def ipc():
    ips = []
    path_out = '../static/video/'
    document_path = Config.SAVE_DOCUMENT_PATH
    try:
        with open(document_path + "ipcConfig.txt", "r+") as  f:
            a = f.readlines()
        for i in a:
            ips.append(i)
    except IOError:
        print('ipc 读取出错')

    if len(ips):
        ipc_name = ''.join(ips[0].split('.'))
    else:
        ipc_name = '0'

    print('ipc_name {}'.format(ipc_name))
    ipc_name = ipc_name.strip()
    #  第一波就灭有的情况
    frame_location = Site.read_site(document_path + "site_{}.txt".format(ipc_name))

    try:
        with open(document_path + "video_save_location.txt", "r+") as  f:
            a = f.readline()
            a = a.strip()
    except IOError:
        a = path_out

    return jsonify({
        'ips': ips,
        'site': frame_location.get_site(),
        'default_ip': ips[0],
        'video_save_location': a
    })


# opencv的编解码能力===》替换当时
@main.route('/steam/')
def steam():
    ipv4 = request.args.get('ip')

    ipc = Onvif_hik(ipv4, 8899, 'admin', '')
    print(ipv4)
    rtsp_uri = 'rtmp://58.200.131.2:1935/livetv/cctv1'
    if ipc.content_cam():
        rtsp_uri = ipc.get_steam_uri()
        print("done")
        return Response(gen(VideoCamera(rtsp_uri)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        # return rtsp_uri

    else:
        print('ip 未找到')
        return "ip 未找到"
    # return Response(gen(VideoCamera(rtsp_uri)),
    #                 mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route('/thread/')
def thread():
    # 创建新线程
    ipv4 = request.args.get('ip')
    if threadsPool.get(ipv4) is not None:
        return ipv4 + '已录制准备'

    ipc = Onvif_hik(ipv4, 8899, 'admin', '')
    print(ipv4)
    rtsp_uri = 'rtmp://58.200.131.2:1935/livetv/cctv1'

    if ipc.content_cam():
        rtsp_uri = ipc.get_steam_uri()
        print("get rtsp done")

        thread1 = myThread(1, rtsp_uri, ipv4)

        # 开启新线程
        thread1.start()
        threadsPool.__setitem__(ipv4, thread1)

        return ipv4 + '已新建录制'
    else:
        print('ip has some errors')
        return 'ip has some errors'
    # thread1 = myThread(1, rtsp_uri, ipv4)
    #
    # # 开启新线程
    # thread1.start()
    # threadsPool.__setitem__(ipv4, thread1)
    # return ipv4 + '已新建录制'


@main.route('/stop/')
def stop():
    ip = request.args.get('ip')
    print(ip)
    result = threadsPool.get(ip)
    if result == None:
        return '该ip并没有在后台执行录制程序'
    else:
        try:
            print('change ExitFlag')
            print(type(result))
            result.stop()
            threadsPool.__delitem__(ip)
            return '已停止' + ip + '的录制'
        except Exception as e:
            print('停止录制线程出现问题')
            return '录制出现问题'


@main.route('/steam/uri/')
def steam_uri():
    ipv4 = request.args.get('ip')

    ipc = Onvif_hik(ipv4, 8899, 'admin', '')
    print(ipv4)
    rtsp_uri = 'rtmp://58.200.131.2:1935/livetv/cctv1'
    if ipc.content_cam():
        rtsp_uri = ipc.get_steam_uri()
        print("get rtsp done")

    return rtsp_uri
