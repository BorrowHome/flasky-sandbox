import json

import cv2
from flask import request
import os
from app.main import main
from app.utils.areas_height import areaRect
from app.utils.areas_height.areaS import ostu
from app.utils.frame.site import Site
from app.utils.frame.sub import PictureSub
from config import Config


@main.route("/area/", methods=['POST'])
def get_volume():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    data = json.loads(request.get_data(as_text=True))
    video_name = data.get('video_name').strip()
    path = image_path + "ipaint_{}.png".format(video_name)
    # imread 的filename 长度有限制。
    print(path)
    s = cv2.imread(path.strip())  # ipaint 是直接减去的图像
    print(s)
    sub = PictureSub()
    t = sub.iblack(s, 220)  # 图像变为黑白两种
    cv2.imwrite(image_path + "iblack_" + video_name + ".png", t)
    path = document_path + "site_{}.txt".format(video_name)
    with open(path, "r+") as f:
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
@main.route("/mosaicarea/", methods=['POST'])
def mosaicarea():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    video_names = []
    path_in = './app/static/video/'
    document_path = Config.SAVE_DOCUMENT_PATH
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in filenames:
            # dir_file_name = os.path.join(dirpath, filename)
            dir_file_name = filename
            if os.path.splitext(dir_file_name)[1] == '.mp4' or '.avi':  # (('./app/static/movie', '.mp4'))
                print(dir_file_name)
                video_names.append(dir_file_name)
    data = json.loads(request.get_data(as_text=True))
    print(video_names)
    FrontVideo_names=[]
    for i in range(len(video_names)):
        FrontVideo_names.append(video_names[i].split('.')[0])
    Frame_areaS=0
    Sand_areaS=0
    Sand_frame_scales=[]
    for video_name in FrontVideo_names:
        path = image_path + "ipaint_{}.png".format(video_name)
        # imread 的filename 长度有限制。
        print(path)
        s = cv2.imread(path.strip())  # ipaint 是直接减去的图像
        sub = PictureSub()
        t = sub.iblack(s, 220)  # 图像变为黑白两种
        cv2.imwrite(image_path + "iblack_" + video_name + ".png", t)
        path = document_path + "site_{}.txt".format(video_name)
        with open(path, "r+") as f:
            a = f.readlines()
            print(a)
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
        frame_area = areaRect.get_frame_area(frame_location.locate_x,
                                             frame_location.locate_y,
                                             frame_location.locate_x + frame_location.move_x,
                                             frame_location.locate_y + frame_location.move_y)
        Frame_areaS+=frame_area
        img = t
        sand_area = ostu(img)
        sand_frame_scale = float(sand_area) / float(frame_area)
        Sand_frame_scales.append(sand_frame_scale*frame_area)
        Sand_areaS+=sand_area

    frame_area=Frame_areaS
    sand_area=Sand_areaS
    sand_frame_scale=0
    for i in Sand_frame_scales:
        sand_frame_scale+=i/frame_area
    print(frame_area)
    print(sand_area)
    print(sand_frame_scale)

    return {
        "frame_area": frame_area,
        "sand_area": sand_area,
        "sand_frame_scale": sand_frame_scale
    }



if __name__ == '__main__':
    s = cv2.imread("back_192168110.png")  # ipaint 是直接减去的图像
    sub = PictureSub()
    t = sub.iblack(s, 220)  # 图像变为黑白两种
    print(t.shape)
