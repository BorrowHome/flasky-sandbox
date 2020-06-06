import cv2


class VideoCam(object):
    def __init__(self, id):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(id)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        success, image = self.video.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def show(self):
        while 1:
            ret, frame = self.video.read()
            cv2.imshow("cap", frame)
            if cv2.waitKey(100) & 0xff == ord('q'):
                break


if __name__ == '__main__':
    came = VideoCam(0)
    came.show()
    info = came.get_frame()
    # print(info)