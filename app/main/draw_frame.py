import cv2
from flask import request, render_template

from app.utils.drawRedrect import pic_to_red
from app.utils.frame import base64_to_png
from app.utils.zuobiao import PictureSub
from config import Config
from . import main


# INFO 2019/12/28 14:46 liliangbin  一页新页进行图片位置的比较。
@main.route("/draw_frame/", methods=["POST", "GET"])
def draw_frame():
    image_path = Config.UPLOAD_IMAGE_PATH
    # 我们把id存放再前端，draw_frame每次都是唯一的
    if request.method == 'POST':
        str = request.form['current_frame']
        img_np = base64_to_png(str)
        cv2.imwrite(image_path + "draw_frame.png", img_np)
        print(img_np.shape)
    else:
        img_np = cv2.imread(image_path + "draw_frame.png")
    return render_template("draw_frame.html", currentframe="draw_frame.png", width=img_np.shape[1],
                           height=img_np.shape[0])


@main.route("/recognize/", methods=['POST', 'GET'])
def recognize():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        str1 = request.form['current_frame']
        img_np = base64_to_png(str1)
        cv2.imwrite(image_path + "origin.png", img_np)
        red_png = pic_to_red(image_path + "origin.png")
        picture_sub = PictureSub()
        src1 = cv2.imread(image_path + red_png)
        locate = picture_sub.left_up(src1)
        locate_remote = picture_sub.right_down(src1)
        move_x = locate_remote['list_x'] - locate['list_x']
        move_y = locate_remote['list_y'] - locate['list_y']
        print(locate['list_x'], locate['list_y'], move_x, move_y)
        with open(document_path + "site_0.txt", 'w') as f:
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
