# -*- coding: utf-8 -*-
import json
import os

import cv2
from flask import request, render_template, redirect, url_for, flash

from app.utils.frame.frame import base64_to_png
from config import Config
from app.main import main


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@main.route('/upload/', methods=['POST'])
def settings():
    videos = request.files.getlist('video')
    print(request.files)
    for video in videos:
        print(video.filename)
        print(video.filename)
        print(video.filename, os.path.abspath(video.filename))
        if allowed_file(video.filename):
            file_path = Config.UPLOAD_PATH + os.sep + os.path.split(os.path.abspath(video.filename))[1]
            video.save(file_path)
        else:
            flash('Wrong file type!' + video.filename, 'danger')
            # return redirect(url_for('.index'))
    flash("Upload successfully!", 'success')  # @hehao
    # video.save(Config.UPLOAD_PATH + video.filename)

    return 'success'


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


# 上传背景图片 并强制转化图片大小  需要重构
@main.route('/image_back/', methods=['POST', 'GET'])
def image_back():
    image_path = Config.UPLOAD_IMAGE_PATH
    print(request.files)
    id = request.form.get('id')
    image = request.files.get('background')
    location = request.form.get('location')
    print(location)
    print('hello world ')
    temfile = 'test.jpg'
    file_path = image_path + 'back_' + id + '.png'
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
