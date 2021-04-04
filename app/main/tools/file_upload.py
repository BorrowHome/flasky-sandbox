# -*- coding: utf-8 -*-
import json
import os

import cv2
from flask import request, flash

from app.main import main
from app.utils.frame.frame import base64_to_png
from config import Config


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@main.route('/save_image/', methods=['POST'])
def save_image():
    image_path = Config.UPLOAD_IMAGE_PATH
    data = json.loads(request.get_data(as_text=True))
    frame = data.get('current_frame')
    video_name = data.get('video_name')
    img_np = base64_to_png(frame)
    # cv2.imwrite(image_path + "info.png", img_np)  对中文路径不友好
    cv2.imencode('.png', img_np)[1].tofile(image_path + "chart_" + video_name + ".png")
    return 'save'


@main.route('/draw_picture/', methods=['POST'])
def save_im():
    image_path = Config.UPLOAD_IMAGE_PATH
    data = json.loads(request.get_data(as_text=True))
    frame = data.get('current_frame')
    video_name = data.get('video_name')
    img_np = base64_to_png(frame)
    cv2.imencode('.png', img_np)[1].tofile(image_path + "drawPicture_video" + ".png")
    return "done"


#  上传的背景图片
@main.route('/FileUpload/', methods=['POST', 'GET'])
def FileUpload():
    images = request.files.getlist('file')
    a = request.files.get('file')
    print(len(images))
    print(images[0])
    filename = request.form.get('mainVideoName')
    print("======>{}".format(filename))
    # TODO // 对图像的后缀以及名字的合法性进行鉴定
    for image in images:
        image_path = Config.UPLOAD_IMAGE_PATH
        print(request.files)
        print('save temp upload back group with  name test.jpg ')
        temfile = 'test.jpg'
        file_path = image_path + 'back_' + filename + '.png'
        image.save(temfile)
        img = cv2.imread(temfile)
        print(type(img))
        shape = img.shape
        width = shape[1]
        temp_scale = 640 / float(width)
        scale = round(temp_scale, 1)
        print("cscale ==" + str(scale))

        newImage = cv2.resize(img, None, fx=scale, fy=scale)
        cv2.imwrite(file_path, newImage)
        print(type(image))

        return '0'


@main.route('/VideoUpload/', methods=['POST', 'GET'])
def VideoUpload():
    videos = request.files.getlist('file')
    video_save_location = Config.SAVE_VIDEO_PATH
    print(len(videos))
    print('upload path === {}'.format(video_save_location))

    for video in videos:
        print('file name ==={}'.format(video.filename))
        if allowed_file(video.filename):
            video.save(video_save_location+video.filename)
            return '1'
        else:
            print('当前file 后缀不支持')
            return '0'

    print('无上传的文件')
    return '0'
