# pip3 install --upgrade onvif_zeep
import time

import requests
import zeep
from onvif import ONVIFCamera
from requests.auth import HTTPDigestAuth

from config import Config


def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


class Onvif_hik(object):
    def __init__(self, ip: str, port: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue  # 很关键 处理的文件
        self.save_path = "./{}T{}.jpg".format(self.ip, str(time.time()))  # 截图保存路径

    def content_cam(self):
        """
        链接相机地址
        :return:
        """
        try:
            self.mycam = ONVIFCamera(self.ip, self.port, self.username, self.password,
                                     wsdl_dir=Config.ONVIF_DEPENDENCE_LOCATION)
            self.media = self.mycam.create_media_service()  # 创建媒体服务
            # print(self.media.GetProfiles())
            self.media_profile = self.media.GetProfiles()[0]  # 获取配置信息
            self.ptz = self.mycam.create_ptz_service()  # 创建控制台服务
            return True
        except Exception as e:
            print(e)
            return False

    def Snapshot(self):
        """
        截图
        :return:
        """
        res = self.media.GetSnapshotUri({'ProfileToken': self.media_profile.token})
        print(res.Uri)
        response = requests.get(res.Uri, auth=HTTPDigestAuth(self.username, self.password))
        with open(self.save_path, 'wb') as f:  # 保存截图
            f.write(response.content)

    def get_steam_uri(self):
        print(self.media_profile.token)
        res = self.media.GetStreamUri(
            {'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'HTTP'}, 'ProfileToken': '002'})
        print(res.Uri)
        # 此处默认拿的是最大的分辨率，我们可以把token 换成001 或是002 ，分辨率会下来
        return res.Uri

    def get_presets(self):
        """
        获取预置点列表
        :return:预置点列表--所有的预置点
        """
        presets = self.ptz.GetPresets({'ProfileToken': self.media_profile.token})  # 获取所有预置点,返回值：list
        return presets

    def goto_preset(self, presets_token: int):
        """
        移动到指定预置点
        :param presets_token: 目的位置的token，获取预置点返回值中
        :return:
        """
        try:
            self.ptz.GotoPreset(
                {'ProfileToken': self.media_profile.token, "PresetToken": presets_token})  # 移动到指定预置点位置
        except Exception as e:
            print(e)

    def zoom(self, zoom: str, timeout: int = 0.1):
        """
        变焦
        :param zoom: 拉近或远离
        :param timeout: 生效时间
        :return:
        """
        request = self.ptz.create_type('ContinuousMove')
        request.ProfileToken = self.media_profile.token
        request.Velocity = {"Zoom": zoom}
        self.ptz.ContinuousMove(request)
        time.sleep(timeout)
        self.ptz.Stop({'ProfileToken': request.ProfileToken})


if __name__ == '__main__':
    test = Onvif_hik('192.168.1.10', 8899, 'admin', '')
    # 端口
    create = test.content_cam()
    if create:
        print('create')
        # test.Snapshot()
        test.get_steam_uri()
    else:
        print("rush ")

# media.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast','Transport':'UDP'},'ProfileToken':token})
# rtsp://192.168.1.10:554/user=admin_password=tlJwpbo6_channel=1_stream=1.sdp?real_stream
# rtsp://192.168.1.10:554/user=admin_password=tlJwpbo6_channel=1_stream=1.sdp?real_stream
# rtsp://192.168.1.10:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream
