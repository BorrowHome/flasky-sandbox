import cv2
from flask import request

from app.main import main
from app.utils.frame.frame import base64_to_png
from config import Config


# INFO 2019/12/28 14:46 liliangbin  新页进行边框坐标的准备。
@main.route("/draw_frame/", methods=["POST"])
def draw_frame():
    image_path = Config.UPLOAD_IMAGE_PATH
    str = request.form['current_frame']
    img_np = base64_to_png(str)
    cv2.imwrite(image_path + "draw_frame.png", img_np)
