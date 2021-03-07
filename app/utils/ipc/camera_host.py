import cv2
import random
import base64
from flask_socketio import emit


class VideoCamera(object):
    def __init__(self, uri):
        print(uri)
        self.video = cv2.VideoCapture(uri)
        print(self.video.isOpened())

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        # image = cv2.flip(image, 180)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def show(self):
        while 1:
            ret, frame = self.video.read()
            cv2.imshow("cap", frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break


class CVClient(object):
    def convert_image_to_jpeg(self, frame):
        # Encode frame as jpeg
        # Encode frame in base64 representation and remove
        # utf-8 encoding

        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def emit_message(self, image):
        print('emit message ========>>>>>>>>>{}'.format(self.name))
        emit(self.name, {'image': self.convert_image_to_jpeg(image)}, namespace='/test')
        return True

    def __init__(self, name, rtmp_location):
        self.run = True
        self.name = name
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
            import time
            time.sleep(3)

    def run_rtsp(self):
        ipcCamera = VideoCamera(self.rtmp_location)
        while self.run:
            image = ipcCamera.get_frame()
            result = self.emit_message(image)
            import time
            time.sleep(3)

    def stop_run(self):
        self.run = False


if __name__ == '__main__':
    came = VideoCamera(0)
    came.show()
    info = came.get_frame()
    # print(info)
