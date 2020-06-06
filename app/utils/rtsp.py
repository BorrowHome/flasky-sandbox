# pip3 install opencv-python

import cv2


# 获取本地摄像头
# folder_path 截取图片的存储目录
def get_img_from_camera_local(folder_path):
    cap = cv2.VideoCapture(0)
    i = 1
    while True:
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        cv2.imwrite(folder_path + str(i) + '.jpg', frame)  # 存储为图像
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
    cap.release()
    cv2.destroyAllWindows()


# 获取网络摄像头，格式：rtsp://username:pwd@ip/
# folder_path 截取图片的存储目录
def get_img_from_camera_net(folder_path, uri):
    print("parpered ")
    cap = cv2.VideoCapture(uri)
    i = 1
    print("in ")
    while True:
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        cv2.imwrite(folder_path + str(i) + '.jpg', frame)  # 存储为图像
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        print("rush ")
    cap.release()
    cv2.destroyAllWindows()


# 测试
if __name__ == '__main__':
    folder_path = './img/'
    # get_img_from_camera_local(folder_path)
    get_img_from_camera_net(folder_path,
                            'rtsp://192.168.1.10:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream')


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
        #image = cv2.flip(image, 180)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
