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
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        videos = request.files.getlist('video')
        print(request.files)

        print("fsdfsfd")
        # TODO // 对图像的后缀以及名字的合法性进行鉴定
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

        return redirect(url_for('.index'))


@main.route('/save_image/', methods=['POST', "GET"])
def save_image():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        frame = data.get('current_frame')
        video_name = data.get('video_name')
        print(type(video_name))
        img_np = base64_to_png(frame)
        # cv2.imwrite(image_path + "info.png", img_np)  对中文路径不友好
        cv2.imencode('.png', img_np)[1].tofile(image_path + "chart_" + video_name + ".png")

    return "done"


@main.route('/image_back/', methods=['POST', 'GET'])
def image_back():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'GET':
        return render_template('index1.html')
    else:
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
        print(type(image))
        if location == 'ipc':
            return redirect(url_for('.ipc'))
        elif location == 'multi_video':
            return redirect(url_for('.multi_video'))
        return redirect('.')
