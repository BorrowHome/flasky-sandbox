import base64

import cv2
import numpy as np
from flask import request, render_template

from app.utils.drawRedrect import pic_to_red
from app.utils.zuobiao import PictureSub
from config import Config
from . import main


# INFO 2019/12/28 14:46 liliangbin  一页新页进行图片位置的比较。
@main.route("/draw_frame/", methods=["POST", "GET"])
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
        cv2.imwrite(image_path + "currentframe.png", img_np)
        print(img_np.shape)
    else:
        img_np = cv2.imread(image_path + "currentframe.png")
    return render_template("draw_frame.html", currentframe="currentframe.png", width=img_np.shape[1],
                           height=img_np.shape[0])


@main.route("/recognize/", methods=['POST', 'GET'])
def recognize():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        str1 = request.form['current_frame']
        str1 = str1.split(',')[1]

        #  在逗号以后的7才是编码数据 前面是协议和格式
        if (len(str1) % 3 == 1):
            str1 += "=="
        elif (len(str1) % 3 == 2):
            str1 += "="

        image = base64.b64decode(str1)
        np_array = np.fromstring(image, np.uint8)
        # 生成cv2 需要的数据类型
        img_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        cv2.imwrite(image_path + "origin.png", img_np)
        red_png = pic_to_red(image_path + "origin.png")
        picture_sub = PictureSub()
        src1 = cv2.imread(red_png)
        locate = picture_sub.left_up(src1)
        locate_remote = picture_sub.right_down(src1)
        move_x = locate_remote['list_x'] - locate['list_x']
        move_y = locate_remote['list_y'] - locate['list_y']
        print(locate['list_x'], locate['list_y'], move_x, move_y)
        with open(document_path + "site.txt", 'w') as f:
            f.write(str(locate['list_x']) + '\n')
            f.write(str(locate['list_y']) + '\n')
            f.write(str(move_x) + '\n')
            f.write(str(move_y) + '\n')

        return {
            "locate_x": locate['list_x'],
            "locate_y": locate['list_y'],
            "move_x": move_x,
            "move_y": move_y
        }
