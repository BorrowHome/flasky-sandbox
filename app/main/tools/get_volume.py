import json

import cv2
from flask import request

from app.main import main
from app.utils.areas_height import areaRect
from app.utils.areas_height.areaS import ostu
from app.utils.frame.site import Site
from app.utils.frame.sub import PictureSub
from config import Config


@main.route("/area/", methods=['POST', 'GET'])
def get_volume():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    data = json.loads(request.get_data(as_text=True))
    video_name = data.get('video_name')
    s = cv2.imread(image_path + "ipaint_" + video_name + ".png")  # ipaint 是直接减去的图像
    sub = PictureSub()
    t = sub.iblack(s, 220)  # 图像变为黑白两种
    # cv2.imwrite(image_path + "iblack_" + id + ".png", t)

    with open(document_path + "site_" + video_name + ".txt", "r+") as f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    frame_area = areaRect.get_frame_area(frame_location.locate_x,
                                         frame_location.locate_y,
                                         frame_location.locate_x + frame_location.move_x,
                                         frame_location.locate_y + frame_location.move_y)

    img = t
    sand_area = ostu(img)
    print(sand_area)
    sand_frame_scale = float(sand_area) / float(frame_area)
    print(sand_frame_scale)
    print("sand_frame_scale")
    return {
        "frame_area": frame_area,
        "sand_area": sand_area,
        "sand_frame_scale": sand_frame_scale,
        "video_name": video_name
    }
