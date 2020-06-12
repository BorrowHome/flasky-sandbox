import cv2


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


if __name__ == '__main__':
    came = VideoCamera(0)
    came.show()
    info = came.get_frame()
    # print(info)
