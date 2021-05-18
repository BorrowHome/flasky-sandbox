import cv2
import numpy as np

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

    def undistort(self, img):
        fx = 1000
        cx = 960
        fy = 1000
        cy = 540
        k1, k2, p1, p2, k3 = -0.195, 0.05, 0, 0, 0

        # 相机坐标系到像素坐标系的转换矩阵
        k = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ])
        # 畸变系数
        d = np.array([
            k1, k2, p1, p2, k3
        ])
        h, w = img.shape[:2]
        mapx, mapy = cv2.initUndistortRectifyMap(k, d, None, k, (w, h), 5)
        return cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    def get_frame(self):
        success, image = self.video.read()
        # cv2.imwrite('C:\abc.jpg', image)
        # image = self.undistort(image)
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


# 处理图像畸变情况
def resolve_change(img):
    fx = 1000
    cx = 960
    fy = 1000
    cy = 540
    k1, k2, p1, p2, k3 = -0.195, 0.05, 0, 0, 0

    # 相机坐标系到像素坐标系的转换矩阵
    k = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    # 畸变系数
    d = np.array([
        k1, k2, p1, p2, k3
    ])
    h, w = img.shape[:2]
    mapx, mapy = cv2.initUndistortRectifyMap(k, d, None, k, (w, h), 5)
    return cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)


if __name__ == '__main__':
    came = VideoCamera(0)
    came.show()
    info = came.get_frame()
    # print(info)
