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
