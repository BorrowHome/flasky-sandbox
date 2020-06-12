from flask import render_template, jsonify

from app.main import main
from app.utils.ipc.li_onvif import Onvif_hik
from app.utils.ipc.multi_thread import threadsPool, myThread
from app.utils.frame.site import Site
from config import Config


@main.route("/multi_ipc_video/", methods=["GET", "POST"])
def multi_ipc_video():
    ips = []

    path_in = './app/static/video/'
    path_out = '../static/video/'
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    with open(document_path + "ipcConfig.txt", "r+") as  f:
        a = f.readlines()
    for i in a:
        ips.append(i)
    try:
        with open(document_path + "site_0.txt", "r+") as  f:
            a = f.readlines()
            print(a)
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    except Exception as e:
        frame_location = Site(0, 0, 0, 0)

    tmp2 = frame_location.locate_y + frame_location.move_y
    tmp1 = frame_location.locate_x + frame_location.move_x
    site_left_top = str(frame_location.locate_x) + ',' + str(frame_location.locate_y)
    site_left_bottom = str(frame_location.locate_x) + ',' + str(tmp2)

    site_right_top = str(tmp1) + ',' + str(frame_location.locate_y)
    site_right_bottom = str(tmp1) + ',' + str(tmp2)

    return render_template('multi_ipc_video.html',
                           ips=ips,
                           site_left_top=site_left_top,
                           site_left_bottom=site_left_bottom,
                           site_right_top=site_right_top,
                           site_right_bottom=site_right_bottom,
                           )


@main.route('/thread_all/')
def thread_all():
    ips = []
    document_path = Config.SAVE_DOCUMENT_PATH
    with open(document_path + "ipcConfig.txt", "r+") as  f:
        a = f.readlines()
    for i in a:
        ips.append(i.strip())
    set_ip = []
    for ipv4 in ips:
        if threadsPool.get(ipv4) is not None:
            print(ipv4, '已建立录制')
            continue

        ipc = Onvif_hik(ipv4, 8899, 'admin', '')
        print(ipv4)
        if ipc.content_cam():
            rtsp_uri = ipc.get_steam_uri()
            print("get rtsp done")

            thread1 = myThread(1, 'new Thread ' + ipv4, rtsp_uri, ipv4)

            # 开启新线程
            thread1.start()
            threadsPool.__setitem__(ipv4, thread1)
            set_ip.append(ipv4)
            continue
        else:
            print('ip has some errors', ipv4)
            continue

    return jsonify(set_ip)


@main.route('/stop_all/')
def stop_all():
    ips = []
    document_path = Config.SAVE_DOCUMENT_PATH
    with open(document_path + "ipcConfig.txt", "r+") as  f:
        a = f.readlines()
    for i in a:
        ips.append(i.strip())
    set_ip = []

    for ipv4 in ips:
        result = threadsPool.get(ipv4)
        if result == None:
            print('change ExitFlag')
            print('该ip未在后台运行', ipv4)
        else:
            try:
                print(type(result))
                result.stop()
                threadsPool.__delitem__(ipv4)
                set_ip.append(ipv4)
                print('已停止' + ipv4 + '的录制')
            except Exception as e:
                print('停止录制线程出现问题' + ipv4)
    return jsonify(set_ip)
