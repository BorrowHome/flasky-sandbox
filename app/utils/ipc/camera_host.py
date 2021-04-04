import cv2

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
        if success:
            # image = cv2.flip(image, 180)  #  转换方向 180 度
            # 存储了对应的文件
            ret, jpeg = cv2.imencode('.jpg', image)
            # cv2.imwrite(filename=self.file_location + self.name.strip() + '.png', img=image)
            return jpeg.tobytes()
        else:
            print('can not get ')
            return None

    def show(self):
        while 1:
            ret, frame = self.video.read()
            cv2.imshow("cap", frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break




if __name__ == '__main__':
    came = VideoCamera(0)
    came.show()
    info = came.get_frame()
    # print(info)
