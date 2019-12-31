from flask import Flask, render_template, Response
import cv2


class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture('E:output.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        m = cv2.rectangle(image, (20, 400), (1400, 810), (0, 0, 255), 3)#################根据坐标画框
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter('E:output12.mp4', fourcc, 20.0, (width, height))
        out.write(image)
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index1.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        #ret, frame = cap.read()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        #m = cv2.rectangle(frame, (20, 400), (1400, 810), (0, 0, 255), 3)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #print(frame)
        #m = cv2.rectangle(frame, (20, 400), (1400, 810), (0, 0, 255), 3)

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.3', debug=True, port = 5000)