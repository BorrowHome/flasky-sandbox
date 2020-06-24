import os
import threading
import time

import cv2

from config import Config

threadsPool = {}


class myThread(threading.Thread):
    def __init__(self, threadID, name, rtsp_uri, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.rtsp_uri = rtsp_uri
        self.ip = ip
        self.exit = False
        video_path = Config.SAVE_VIDEO_PATH
        document_path = Config.SAVE_DOCUMENT_PATH
        currentTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

        with open(document_path + "video_save_location.txt", "r+") as  f:
            a = f.readline()
            file_location = a.strip()
        print(a)
        if (os.path.exists(file_location)):
            print("rush")
            self.save_path = file_location + "{}-{}.mp4".format(self.ip, str(currentTime))
        else:
            self.save_path = video_path + "{}-{}.mp4".format(self.ip, str(currentTime))

    def run(self):
        print("开始线程：" + self.name)
        self.print_time()
        # while self.exit:
        #     print('running   ' + self.name)
        #     time.sleep(3)
        print("退出线程：" + self.name)

    def print_time(self):
        cap = cv2.VideoCapture(self.rtsp_uri)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        # 获取cap视频流的每帧大小
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print(size)

        fourcc = cv2.VideoWriter_fourcc(*'avc1')

        print(self.save_path)
        outVideo = cv2.VideoWriter(self.save_path, fourcc, fps, size)
        if cap.isOpened():
            rval, frame = cap.read()
            print('true  info  ')
        else:
            rval = False
            print('False')
        c = 1
        while rval:
            if self.exit:
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
            # print('currentFrame==', c, "  " + self.ip)
            c = c + 1

    def stop(self):
        print('change exit  value to  false')
        self.exit = True
        print(self.save_path)

    def __del__(self):
        self.stop()


# 在应用起来的时候会启动线程
def changeExitFlag():
    global exitFlag
    exitFlag = 1
