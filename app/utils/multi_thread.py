import threading
import time

import cv2

from config import Config

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, rtsp_uri, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.rtsp_uri = rtsp_uri
        self.ip = ip

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.rtsp_uri, self.ip)
        print("退出线程：" + self.name)


def print_time(rtsp_uri, ip):
    cap = cv2.VideoCapture(rtsp_uri)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    # 获取cap视频流的每帧大小
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video_path = Config.SAVE_VIDEO_PATH
    save_path = video_path + "{}T{}.mp4".format(ip, str(time.time()))
    outVideo = cv2.VideoWriter(save_path, fourcc, fps, size)
    if cap.isOpened():
        rval, frame = cap.read()
        print('true')
    else:
        rval = False
        print('False')
    c = 1
    while rval:
        if exitFlag:
            print('stop')
            cap.release()
            outVideo.release()
            cv2.destroyAllWindows()

            return
        rval, frame = cap.read()
        # cv2.imshow('test', frame)
        # 每间隔20帧保存一张图像帧
        # if tot % 20 ==0 :
        #   cv2.imwrite('cut/'+'cut_'+str(c)+'.jpg',frame)
        #   c+=1
        # 使用VideoWriter类中的write(frame)方法，将图像帧写入视频文件
        outVideo.write(frame)
        print('currentFrame==', c)
        c = c + 1


# 在应用起来的时候会启动线程
def changeExitFlag():
    global exitFlag
    exitFlag = 1
