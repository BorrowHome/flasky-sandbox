import os

from flask import render_template

from app.utils.frame.site import Site
from config import Config
from app.main import main
from flask import jsonify


# 现在相当于每次我们添加一个id来处理，常规就默认id为0 如果是多个项目则是为1 2 3 4 .。。。。。

@main.route("/multi_video/", methods=["GET", "POST"])
def multi_video():
    video_names = []
    path_in = './app/static/video/'
    path_out = '../static/video/'
    document_path = Config.SAVE_DOCUMENT_PATH
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in filenames:
            # dir_file_name = os.path.join(dirpath, filename)
            dir_file_name = filename
            if os.path.splitext(dir_file_name)[1] == '.mp4':  # (('./app/static/movie', '.mp4'))
                print(dir_file_name)
                video_names.append(path_out + dir_file_name)
    with open(document_path + "site_video.txt", "r+") as  f:
        a = f.readlines()
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    video_src = video_names[0]
    tmp2 = frame_location.locate_y + frame_location.move_y
    tmp1 = frame_location.locate_x + frame_location.move_x
    site_left_top = [str(frame_location.locate_x), str(frame_location.locate_y)]
    site_left_bottom = [str(frame_location.locate_x), str(tmp2)]

    site_right_top = [str(tmp1), str(frame_location.locate_y)]
    site_right_bottom = [str(tmp1), str(tmp2)]

    return jsonify(
        {
            'video_names': video_names,
            'site': {
                'site_left_top': site_left_top,
                'site_left_bottom': site_left_bottom,
                'site_right_top': site_right_top,
                'site_right_bottom': site_right_bottom,
            },
            'video_src': video_src
        }
    )
