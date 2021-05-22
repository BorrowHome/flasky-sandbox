from flask import jsonify

from app.main import main
from app.utils.ipc.ipc_read import read_ips
from app.utils.ipc.li_onvif import Onvif_hik
from app.utils.ipc.multi_thread import threadsPool, myThread
from config import Config


# 录制所有视频
@main.route('/thread_all/')
def thread_all():
    ips = []
    document_path = Config.SAVE_DOCUMENT_PATH
    ips = read_ips()
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

            thread1 = myThread(1, rtsp_uri, ipv4)

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
    ips = read_ips()
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
