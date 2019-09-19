# -*- coding: utf-8 -*-

from flask import request, render_template, redirect, url_for

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
            video.save(Config.UPLOAD_PATH + video.filename)

        return redirect(url_for('.index'))
