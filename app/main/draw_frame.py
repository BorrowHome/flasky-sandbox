import base64

import cv2
import numpy as np
from flask import request, render_template

from config import Config
from . import main


# INFO 2019/12/28 14:46 liliangbin  一页新页进行图片位置的比较。
@main.route("/draw_frame", methods=["POST", "GET"])
def draw_frame():
    image_path = Config.UPLOAD_IMAGE_PATH

    if request.method == 'POST':
        str = request.form['current_frame']
        str = str.split(',')[1]

        #  在逗号以后的7才是编码数据 前面是协议和格式
        if (len(str) % 3 == 1):
            str += "=="
        elif (len(str) % 3 == 2):
            str += "="

        image = base64.b64decode(str)
        np_array = np.fromstring(image, np.uint8)
        # 生成cv2 需要的数据类型
        img_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        cv2.imwrite(image_path + "/currentframe.png", img_np)
        print(img_np.shape)
    else:
        img_np = cv2.imread(image_path + "/currentframe.png")
        print(img_np.shape)
    return render_template("draw_frame.html", currentframe="currentframe.png", width=img_np.shape[1],
                           height=img_np.shape[0])


@main.route("/recognize")
def recognize_coordinate():
    if request.method == 'POST':
        str = request.form['current_frame']
        str = str.split(',')[1]

        #  在逗号以后的7才是编码数据 前面是协议和格式
        if (len(str) % 3 == 1):
            str += "=="
        elif (len(str) % 3 == 2):
            str += "="

        image = base64.b64decode(str)
        np_array = np.fromstring(image, np.uint8)
        # 生成cv2 需要的数据类型
        img_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

