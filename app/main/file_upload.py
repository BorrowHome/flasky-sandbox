# -*- coding: utf-8 -*-
import os

import cv2
from flask import request, render_template, redirect, url_for, flash

from app.utils.frame import base64_to_png
from config import Config
from . import main


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@main.route('/upload/', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        videos = request.files.getlist('video')
        # TODO // 对图像的后缀以及名字的合法性进行鉴定
        for video in videos:
            print(video.filename)
            print(video.filename)
            print(video.filename, os.path.abspath(video.filename))
            if allowed_file(video.filename):
                file_path = Config.UPLOAD_PATH + os.sep + os.path.split(os.path.abspath(video.filename))[1]
                video.save(file_path)
            else:
                flash('Wrong file type!', 'danger')
                return redirect(url_for('.index'))
        flash("Upload successfully!", 'success')  # @hehao
        # video.save(Config.UPLOAD_PATH + video.filename)

        return redirect(url_for('.index'))


@main.route('/save_image/', methods=['POST', "GET"])
def save_image():
    image_path = Config.UPLOAD_IMAGE_PATH
    document_path = Config.SAVE_DOCUMENT_PATH
    if request.method == 'POST':
        str = request.form['current_frame']
        id = request.form['id']
        img_np = base64_to_png(str)
        # cv2.imwrite(image_path + "info.png", img_np)  对中文路径不友好
        cv2.imencode('.png', img_np)[1].tofile(image_path + "chart_" + id + ".png")

    return "done"
