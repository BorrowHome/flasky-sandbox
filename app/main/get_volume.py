import cv2
from flask import request

from app.utils import areaRect
from app.utils.areaS import ostu
from app.utils.site import Site
from config import Config
from . import main


@main.route("/get_volume/", methods=['POST', 'GET'])
def get_volume():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    id = request.form['id']
    with open(document_path + "site_" + id + ".txt", "r+") as f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    frame_area = areaRect.get_frame_area(frame_location.locate_x,
                                         frame_location.locate_y,
                                         frame_location.locate_x + frame_location.move_x,
                                         frame_location.locate_y + frame_location.move_y)

    # helen = Helen_formula()
    # # 沙子坐标
    # points = []
    # sand_coordinate = csv.reader(open('sand.csv', 'r'))
    # # 单路正向
    # # 回路
    # temp = 352 - (frame_location.locate_y + frame_location.move_y)
    # print(temp)
    # print("info\n")
    # sum = 0
    # for volume in sand_coordinate:
    #     points.append(Point(int(volume[0]), int(volume[1])))
    #     sum = sum + 1
    #
    # for tmp in range(sum, 0, -1):
    #     points.append(Point(points[tmp - 1].x, temp))
    #     sand_area = helen.get_area_of_poly_gon(points)
    sand_area = 0
    img = cv2.imread(image_path + "iblack_" + id + ".png")
    sand_area = ostu(img)
    sand_frame_scale = float(sand_area) / float(frame_area)
    print(sand_frame_scale)
    print("sand_frame_scale")
    return {
        "frame_area": frame_area,
        "sand_area": sand_area,
        "sand_frame_scale": sand_frame_scale,
        "id": id
    }
