import threading

import cv2
import random
import base64

from config import Config


class VideoCamera(object):
    def __init__(self, uri, name='name'):
        print(uri)
        self.video = cv2.VideoCapture(uri)
        print(self.video.isOpened())
        self.file_location = Config.UPLOAD_IMAGE_PATH
        self.name = name

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        # image = cv2.flip(image, 180)
        # 存储了对应的文件
        ret, jpeg = cv2.imencode('.jpg', image)
        cv2.imwrite(filename=self.file_location + self.name.strip() + '.png', img=image)
        return jpeg.tobytes()

    def show(self):
        while 1:
            ret, frame = self.video.read()
            cv2.imshow("cap", frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break


class CVClient(threading.Thread):
    def convert_image_to_jpeg(self, frame):
        # Encode frame as jpeg
        # Encode frame in base64 representation and remove
        # utf-8 encoding

        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def emit_message(self, image):
        print('emit message ========>>>>>>>>>{}'.format(self.name))
        # emit(self.name, {'image': self.convert_image_to_jpeg(image), 'time': "time"}, namespace='/test')
        self.socketio.emit(self.name, {'time': "time"}, namespace='/test', broadcast=True)
        print('emit done ====>{}'.format(self.name))
        return True

    def __init__(self, name, rtmp_location, socketio):
        threading.Thread.__init__(self)
        self.exit = True
        self.name = name
        self.socketio = socketio
        self.rtmp_location = rtmp_location

    def get_frame(self):
        id = random.randint(0, 3)
        image = cv2.imread('./app/static/image/current_{}.png'.format(id))
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        return frame

    def run_image(self):
        while self.run:
            image = self.get_frame()
            result = self.emit_message(image)
            self.socketio.sleep(1)

    def run_rtsp(self):
        ipcCamera = VideoCamera(self.rtmp_location)
        while self.exit:
            image = ipcCamera.get_frame()
            result = self.emit_message(image)

    def run(self):
        print('run thread {}'.format(self.name))
        self.run_rtsp()

    def stop_run(self):
        self.exit = False


if __name__ == '__main__':
    came = VideoCamera(0)
    came.show()
    info = came.get_frame()
    # print(info)
