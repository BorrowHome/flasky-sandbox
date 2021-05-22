import os

from config import Config


def read_ips():
    document_path = Config.SAVE_DOCUMENT_PATH
    ips = []
    try:
        with open(document_path + "ipcConfig.txt", "r+", encoding="utf8") as  f:
            a = f.readlines()
        for i in a:
            ips.append(i.split(',')[0])
    except IOError:
        print('ipc 读取出错')

    return ips


def read_ip_names():
    document_path = Config.SAVE_DOCUMENT_PATH
    ipnames = []
    try:
        with open(document_path + "ipcConfig.txt", "r+", encoding="utf8") as  f:
            a = f.readlines()
        for i in a:
            if len(i.split(',')) == 2:
                ipnames.append(i.split(',')[-1].strip('\n'))
            else:
                ipnames.append(i.split(',')[0])
    except IOError:
        print('ipc 读取出错')
    return ipnames


def read_video_names(location='video'):
    path_in = Config.SAVE_VIDEO_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    video_names = []
    if 'video' == location:
        for dirpath, dirnames, filenames in os.walk(path_in):
            for filename in filenames:
                dir_file_name = filename
                if os.path.splitext(dir_file_name)[1] == '.mp4' or '.avi':  # (('./app/static/movie', '.mp4'))
                    print(dir_file_name)
                    video_names.append(dir_file_name)

        print(video_names)
        for i in range(len(video_names)):
            video_names[i] = video_names[i].split('.mp4')[0]
    else:
        ips = read_ips()
        for i in range(len(ips)):
            video_names.append(''.join(ips[i].split('.')))

    return video_names
